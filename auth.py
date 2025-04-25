import json
import bcrypt
import os

USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password, role="user"):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {"password": hashed, "role": role}
    save_users(users)
    return True, "User registered successfully."

def authenticate_user(username, password):
    users = load_users()
    if username in users and bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        return True, users[username]["role"]
    return False, None

def delete_user(username):
    users = load_users()
    if username in users:
        users.pop(username)
        save_users(users)
        return True
    return False

def get_all_users():
    return load_users()
