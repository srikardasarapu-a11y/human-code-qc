import hashlib
import os

def hash_bytes(data: bytes) -> str:
    """Returns the lowercase hexadecimal SHA-256 hash of the given bytes."""
    return hashlib.sha256(data).hexdigest()

def hash_text(text: str, encoding: str = "utf-8") -> str:
    """Returns the lowercase hexadecimal SHA-256 hash of the given string encoded to bytes."""
    return hash_bytes(text.encode(encoding))

def hash_file(path: str, chunk_size: int = 8192) -> str:
    """
    Returns the lowercase hexadecimal SHA-256 hash of a file's contents,
    processed in chunks to prevent large memory overhead.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
        
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read the file in chunks to handle arbitrarily large files safely.
        for byte_block in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(byte_block)
            
    return sha256_hash.hexdigest()
