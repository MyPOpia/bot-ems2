import json
import os

DATA_FOLDER = "data"
PROFILE_FILE = os.path.join(DATA_FOLDER, "profiles.json")

def init_storage():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w") as f:
            json.dump({}, f)

def load_profiles():
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)

def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

def get_or_create_profile(user_id):
    profiles = load_profiles()
    user_id = str(user_id)
    if user_id not in profiles:
        profiles[user_id] = {
            "nom": "",
            "prenom": "",
            "heures_service": 0.0,  # stocké en secondes
            "reanimations": {"nord": 0, "sud": 0, "fantome": []},
            "soins": {"nord": 0, "sud": 0},
            "absences": []
        }
        save_profiles(profiles)
    return profiles[user_id]

def update_profile(user_id, new_data):
    profiles = load_profiles()
    profiles[str(user_id)] = new_data
    save_profiles(profiles)

async def create_profile(user_id, nom, prenom):
    profiles = load_profiles()
    user_id = str(user_id)
    if user_id not in profiles:
        profiles[user_id] = {
            "nom": nom,
            "prenom": prenom,
            "heures_service": 0.0,
            "reanimations": {"nord": 0, "sud": 0, "fantome": []},
            "soins": {"nord": 0, "sud": 0},
            "absences": []
        }
        save_profiles(profiles)

async def has_profile(user_id):
    profiles = load_profiles()
    return str(user_id) in profiles
