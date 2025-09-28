import json
import os

def load_json(filepath: str, default=None):
    """Safely load JSON file, return default if not exists."""
    if not os.path.exists(filepath):
        return default or {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath: str, data: dict):
    """Write dictionary to JSON file with pretty format."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
