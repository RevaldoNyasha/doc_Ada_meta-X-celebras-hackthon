Doctor Chatbot
Project Overview

This project is a medical assistant chatbot named "Dr. Ada" that provides health advice, symptom assessment, and helps users find nearby medical facilities. The application uses a FastAPI backend with a simple web frontend to deliver helpful guidance.

It’s built with Cerebras Llama AI, a FastAPI backend, and a lightweight web frontend, ensuring accurate, safe, and accessible medical support

Key Features

Symptom Assessment: Analyzes user symptoms and provides appropriate advice.

Home Remedies: Suggests safe, evidence-based home remedies for common ailments.

Facility Locator: Finds nearest hospitals, clinics, and pharmacies using geolocation.

Web Interface: Clean, user-friendly frontend for easy interaction.

Architecture

The application follows a modular architecture:

Backend (FastAPI): Handles API endpoints and logic.

Frontend: Simple HTML/CSS/JavaScript interface.

Agents: Modules for doctor logic and context management.

Context: JSON files containing medical knowledge, symptoms, remedies, and facility data.

Utils: Helper functions for context loading and safety checks.

Dependencies and Installation

Prerequisites

Python 3.11 or higher

Docker (optional, for containerized deployment)

Installation

Clone the repository or ensure all project files are in place.

Install Python dependencies:

pip install -r requirements.txt


Set up environment variables if needed:

cerebras API key 

Libraries Used

FastAPI: Web framework for building API endpoints.

Uvicorn: ASGI server for running the application.

Python Multipart: Handles multipart/form-data requests.

..............................................................

How to Run
Local Development
pip install -r requirements.txt
python Doctor.py


Open http://127.0.0.1:8000
 in your browser to access the chatbot.

Docker Deployment
docker build -t doctor-chatbot .
docker run -p 8000:8000 doctor-chatbot


