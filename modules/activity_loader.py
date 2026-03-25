import json

def load_activity(file_path):
    """
    Loads activity from JSON file
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    return data  # your JSON is single activity