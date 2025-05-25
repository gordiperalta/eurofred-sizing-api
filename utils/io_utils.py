import os
import json


def load_user_input(path):
    full_path = os.path.abspath(path)
    print(f"📄 Loading user input from: {full_path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
