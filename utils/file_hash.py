
import hashlib

def compute_file_hash(file_bytes: bytes) -> str:
    """
    Generate SHA-256 hash of file content.
    Used to detect duplicate files.
    """
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()




