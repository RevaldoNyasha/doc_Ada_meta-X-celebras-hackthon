const chatDiv = document.getElementById("chat");
const inputForm = document.getElementById("inputForm");
const inputText = document.getElementById("inputText");
const sendBtn = document.getElementById("sendBtn");
const locationBtn = document.getElementById("locationBtn");
locationBtn.textContent = "Select Location";
const mapModal = document.getElementById("mapModal");
const closeMap = document.getElementById("closeMap");
let map;
let selectedLat, selectedLon;

function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatDiv.appendChild(msgDiv);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

function checkForEmergency(reply) {
    const emergencyKeywords = ["seek immediate medical help", "emergency", "difficulty breathing", "chest pain", "persistent vomiting", "severe dehydration", "loss of consciousness", "convulsions", "select your location", "nearest facility"];
    return emergencyKeywords.some(keyword => reply.toLowerCase().includes(keyword));
}

inputForm.onsubmit = async (e) => {
    e.preventDefault();
    const userMessage = inputText.value.trim();
    if (!userMessage) return;

    appendMessage(userMessage, "user");
    inputText.value = "";
    sendBtn.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        });
        const data = await response.json();
        if (data.reply) {
            appendMessage(data.reply, "bot");
            if (data.hide_location_button) {
                locationBtn.style.display = "none";
            } else if (checkForEmergency(data.reply)) {
                locationBtn.style.display = "block";
            } else {
                locationBtn.style.display = "none";
            }
        } else {
            appendMessage("Sorry, no response from server.", "bot");
        }
    } catch (err) {
        appendMessage("Error communicating with server.", "bot");
    } finally {
        sendBtn.disabled = false;
        inputText.focus();
    }
};

locationBtn.onclick = () => {
    mapModal.style.display = "block";
    if (!map) {
        // Initialize map centered on Zimbabwe
        map = L.map('map').setView([-19.0154, 29.1549], 7); // Zimbabwe center, zoomed in
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        map.on('click', async (e) => {
            selectedLat = e.latlng.lat;
            selectedLon = e.latlng.lng;

            // Get nearest facility
            try {
                const response = await fetch("/nearest", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ lat: selectedLat, lon: selectedLon })
                });
                const facility = await response.json();
                if (facility.error) {
                    appendMessage(facility.error, "bot");
                } else if (facility.name) {
                    const rec = `Based on the location you provided, you should visit the nearest ${facility.type}: ${facility.name}, located at ${facility.address}. Phone: ${facility.phone}`;
                    appendMessage(`Selected location: ${selectedLat.toFixed(4)}, ${selectedLon.toFixed(4)}`, "user");
                    appendMessage(rec, "bot");
                } else {
                    appendMessage("No nearby facilities found.", "bot");
                }
            } catch (err) {
                appendMessage("Error finding nearest facility.", "bot");
            }

            mapModal.style.display = "none";
            locationBtn.style.display = "none";
        });
    }
};

closeMap.onclick = () => {
    mapModal.style.display = "none";
};
