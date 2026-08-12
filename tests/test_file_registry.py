import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.file_registry as fr


def test_registered_and_indexed_hashes_are_separate(tmp_path):
    fr.HASH_REGISTRY_PATH = str(tmp_path / "registered_hashes.json")
    fr.INDEXED_HASH_REGISTRY_PATH = str(tmp_path / "indexed_hashes.json")

    assert fr.is_hash_registered("abc123") is False
    assert fr.is_hash_indexed("abc123") is False

    fr.mark_hash_registered("abc123")
    assert fr.is_hash_registered("abc123") is True
    assert fr.is_hash_indexed("abc123") is False

    fr.mark_hash_indexed("abc123")
    assert fr.is_hash_indexed("abc123") is True

    assert fr.is_hash_registered("xyz999") is False
    assert fr.is_hash_indexed("xyz999") is False
