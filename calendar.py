import json
import os

EVENT_FILE = "events.json"

def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_events(data):
    with open(EVENT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_events(username="default_user"):
    data = load_events()
    return data.get(username, [])

def add_event(username, event):
    data = load_events()
    data.setdefault(username, []).append(event)
    save_events(data)

def delete_event(username, index):
    data = load_events()
    if username in data and 0 <= index < len(data[username]):
        data[username].pop(index)
        save_events(data)
