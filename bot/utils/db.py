import json
import os

DATA_FILE = "data.json"

def load_data():
    """Load existing registrations from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    """Save all registration data to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_user(name, phone):
    """Add a new user's registration info."""
    data = load_data()
    user_entry = {"name": name, "phone": phone}
    data.append(user_entry)
    save_data(data)
