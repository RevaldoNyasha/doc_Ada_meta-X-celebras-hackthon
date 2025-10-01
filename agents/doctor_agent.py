 # agents/doctor_agent.py

import os
from pathlib import Path
import json
from math import radians, cos, sin, asin, sqrt

# --- Load Context Function ---
def load_context():
    """Load all files from context directory except facility files"""
    context_dir = Path("context")
    context_dir.mkdir(exist_ok=True)

    facility_files = ["hospitals.json", "clinics.json", "pharmacies.json"]
    all_content = ""
    for file_path in context_dir.glob("*"):
        if file_path.is_file() and file_path.name not in facility_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                all_content += f"\n=== {file_path.name} ===\n{content}\n"
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")
    return all_content.strip() or "No context files found"

def load_facilities():
    facilities = []
    for file_name in ["hospitals.json", "clinics.json", "pharmacies.json"]:
        try:
            with open(f"context/{file_name}", "r", encoding="utf-8") as f:
                facilities.extend(json.load(f))
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    return facilities

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

# --- Doctor Agent ---
class DoctorAgent:
    def __init__(self):
        # Agent properties
        self.name = "Dr. Ada"

        # Load context files
        context = load_context()
        self.facilities = load_facilities()
        print(f"📄 Context loaded: {len(context)} characters")
        print(f"🏥 Facilities loaded: {len(self.facilities)}")

        # Facilities list
        facilities_text = "\n".join([f"- {h['name']} ({h['type']}): {h['address']}" for h in self.facilities])

        # Instructions define response style
        self.instructions = f"""
                        You are {self.name}, a friendly and compassionate AI doctor.

                        Conversation Flow:
                        1. Start with a warm greeting:
                        "Hello! I’m {self.name}, your health assistant. How are you feeling today? What seems to be the problem?"
                        2. After the user shares symptoms, assess and respond accordingly.

                        Behavior Guidelines:
                        - Speak in simple, clear language suitable for patients.
                        - Use only information from the provided context files.
                        - Prioritize emergencies: For emergencies as listed in emergency.json (including difficulty breathing, chest pain, persistent vomiting, severe dehydration, loss of consciousness, convulsions, severe bleeding, sudden weakness or numbness, sudden severe headache, severe abdominal pain, persistent dizziness or fainting), immediately instruct the user to seek immediate medical help and recommend selecting location for nearest facility. Do not loop back to asking about location repeatedly.
                        - Track user state: If location has been provided, do not ask for it again. If an emergency is active, focus on guiding to nearest facility without repetition.
                        - Do not ask the same question twice unless the user skipped it.
                        - For emergencies, show guidance and contacts/nearest branch, then ask for location ONCE if needed.
                        - For mild symptoms, suggest safe home remedies from the context with timelines if available (e.g., apply for 15 minutes, take every 4 hours).
                        - Only recommend visiting a clinic or pharmacy if the remedy requires buying medication or professional help, and then ask for location to find the nearest.
                        - Do not ask for the user's location unless recommending to visit a clinic or pharmacy for medication or in emergencies.
                        - If the user asks about something not in the context, reply with: "I don’t have that information."
                        - Always be polite, encouraging, and patient.
                        - Limit each reply to 500 characters.
                        - After the initial greeting, continue the conversation naturally without repeating introductions.
                        - If recommending to visit, suggest selecting location for nearest facility.

                        Available Hospitals, Clinics, Pharmacies:
        {facilities_text}

        Context:
        {context}
        """
