import json
import os
from config import HASH_REGISTRY_PATH


def _load_registry(path):
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return set(data) if isinstance(data, list) else set()
    except (json.JSONDecodeError, TypeError, ValueError):
        return set()


def _save_registry(path, hashes: set):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(sorted(hashes), f)


def load_hashes():
    return _load_registry(HASH_REGISTRY_PATH)


def save_hashes(hashes: set):
    _save_registry(HASH_REGISTRY_PATH, set(hashes))


def is_hash_registered(file_hash: str) -> bool:
    return file_hash in load_hashes()


def mark_hash_registered(file_hash: str):
    hashes = load_hashes()
    hashes.add(file_hash)
    save_hashes(hashes)


INDEXED_HASH_REGISTRY_PATH = os.path.join(
    os.path.dirname(HASH_REGISTRY_PATH), "indexed_file_hashes.json"
)


def load_indexed_hashes():
    return _load_registry(INDEXED_HASH_REGISTRY_PATH)


def save_indexed_hashes(hashes: set):
    _save_registry(INDEXED_HASH_REGISTRY_PATH, set(hashes))


def is_hash_indexed(file_hash: str) -> bool:
    return file_hash in load_indexed_hashes()


def mark_hash_indexed(file_hash: str):
    hashes = load_indexed_hashes()
    hashes.add(file_hash)
    save_indexed_hashes(hashes)
