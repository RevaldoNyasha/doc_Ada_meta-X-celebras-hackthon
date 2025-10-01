import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from agents.doctor_agent import DoctorAgent
from cerebras.cloud.sdk import Cerebras
from math import radians, cos, sin, asin, sqrt
import json

app = FastAPI()

# Serve frontend
@app.get("/")
def serve_home():
    return FileResponse("frontend/home.html")

@app.get("/chat")
def serve_chat():
    return FileResponse("frontend/index.html")

@app.get("/main.js")
def serve_js():
    return FileResponse("frontend/main.js")

@app.get("/doctor.gif")
def serve_gif():
    return FileResponse("frontend/doctor.gif")

# Initialize Cerebras client
client = Cerebras(
    api_key=os.environ.get("csk-vtjh4mhkcnhcwfh3exrjydxhx2emkrtct9kj6chn36y23fxy")
)

doctor_agent = DoctorAgent()

# Load emergency keywords
with open("context/emergency.json", "r") as f:
    emergency_data = json.load(f)
emergency_keywords = [symptom["symptom"].lower() for symptom in emergency_data["emergency_symptoms"]]

# Global conversation history (for single user demo)
conversation = [{"role": "system", "content": doctor_agent.instructions}]

# Global user state (for single user demo)
location_provided = False
emergency_active = False

def haversine(lon1, lat1, lon2, lat2):
    # Calculate the great circle distance between two points on the earth (specified in decimal degrees)
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

@app.post("/nearest")
async def nearest_facility(request: Request):
    global location_provided
    data = await request.json()
    user_lat = data.get("lat")
    user_lon = data.get("lon")
    if user_lat is None or user_lon is None:
        return JSONResponse({"error": "Missing lat or lon"})

    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
    except ValueError:
        return JSONResponse({"error": "Invalid lat or lon"})

    # Set location provided
    location_provided = True

    # Find nearest
    nearest = None
    min_dist = float('inf')
    for h in doctor_agent.facilities:
        dist = haversine(user_lon, user_lat, h["longitude"], h["latitude"])
        if dist < min_dist:
            min_dist = dist
            nearest = h

    if nearest:
        return JSONResponse({
            "name": nearest["name"],
            "address": nearest["address"],
            "phone": nearest.get("phone", "N/A"),
            "type": nearest["type"]
        })
    else:
        return JSONResponse({"error": "No facilities found"})

@app.post("/chat")
async def chat_endpoint(request: Request):
    global emergency_active, location_provided
    data = await request.json()
    user_message = data.get("message", "").lower()
    if not user_message:
        return JSONResponse({"reply": "Please send a message."})

    # Check for emergency
    is_emergency = any(keyword in user_message for keyword in emergency_keywords)
    if is_emergency and not emergency_active:
        emergency_active = True
        # Immediate guidance
        guidance = emergency_data["instructions"] + " Please select your location to find the nearest hospital."
        return JSONResponse({"reply": guidance, "hide_location_button": location_provided})

    # Update system prompt with state
    state_info = ""
    if emergency_active and not location_provided:
        state_info = " The user has reported an emergency. Ask for location to find nearest facility if not already asked."
    elif location_provided:
        state_info = " The user's location has been provided. Do not ask for location again."
    conversation[0]["content"] = doctor_agent.instructions + state_info

    # Append user message
    conversation.append({"role": "user", "content": user_message})

    # Keep only last 20 messages to avoid too long
    if len(conversation) > 21:  # system + 20
        conversation.pop(1)  # remove oldest user/assistant

    response = client.chat.completions.create(
        messages=conversation,
        model="llama-3.3-70b",
        stream=False,
        max_completion_tokens=100,  # Limit tokens to control length
        temperature=0.2,
        top_p=1
    )

    reply_text = response.choices[0].message.content
    # Limit to 500 characters
    if len(reply_text) > 500:
        reply_text = reply_text[:500] + "..."

    # Append bot reply
    conversation.append({"role": "assistant", "content": reply_text})

    return JSONResponse({"reply": reply_text, "hide_location_button": location_provided})
