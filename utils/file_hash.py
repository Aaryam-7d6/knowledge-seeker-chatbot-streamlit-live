
import hashlib
from typing import Union, IO


def compute_file_hash(file_bytes: Union[bytes, bytearray, memoryview, str, IO]) -> str:
    """
    Generate SHA-256 hash of file content.

    Accepts bytes, bytearray, memoryview, str (will be encoded to utf-8),
    or a file-like object (read() will be called).
    """
    # Normalize input to bytes
    if isinstance(file_bytes, memoryview):
        data = file_bytes.tobytes()
    elif isinstance(file_bytes, bytearray):
        data = bytes(file_bytes)
    elif isinstance(file_bytes, bytes):
        data = file_bytes
    elif isinstance(file_bytes, str):
        data = file_bytes.encode("utf-8")
    elif hasattr(file_bytes, "read"):
        # file-like object
        data = file_bytes.read()
        if isinstance(data, memoryview):
            data = data.tobytes()
        elif isinstance(data, bytearray):
            data = bytes(data)
        elif isinstance(data, str):
            data = data.encode("utf-8")
    else:
        raise TypeError("compute_file_hash expects bytes-like input, a str, or a file-like object")

    if not isinstance(data, (bytes,)):
        raise TypeError("compute_file_hash normalization failed; expected bytes after normalization")

    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()




