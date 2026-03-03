import json
import os

def save_data(filename, data):
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_data(filename):
    filepath = os.path.join('data', filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)
