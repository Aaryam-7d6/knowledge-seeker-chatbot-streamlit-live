import json
import os
from config import HASH_REGISTRY_PATH

def load_hashes():
    if not os.path.exists(HASH_REGISTRY_PATH):
        return set()
    with open(HASH_REGISTRY_PATH, "r") as f:
        return set(json.load(f))

def save_hashes(hashes: set):
    os.makedirs(os.path.dirname(HASH_REGISTRY_PATH), exist_ok=True)
    with open(HASH_REGISTRY_PATH, "w") as f:
        json.dump(list(hashes), f)
