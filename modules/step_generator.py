# core/step_generator.py

from core.activity_loader import load_activities

def generate_steps(user_input):
    """
    Matches user input with activity keywords
    and returns steps
    """

    user_input = user_input.lower()

    activities = load_activities()

    for activity in activities:
        for keyword in activity["keywords"]:
            if keyword in user_input:
                return activity["steps"]

    return ["No matching activity found"]