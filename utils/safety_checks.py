def check_emergency(symptoms, emergency_list):
    """
    Check if any symptom matches emergency symptoms.
    """
    for s in symptoms:
        if s.lower() in [e.lower() for e in emergency_list]:
            return True
    return False
