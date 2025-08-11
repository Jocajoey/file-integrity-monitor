"""
Hash Utils for calculating file hashes.
Checklist:
1. Define chunk size for reading files.
2. Implement SHA256 hash function.
3.Ensure reading files in chunks to handle large files efficiently.
"""


import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024  # 1 MB

def sha256_file(path: Path) -> str:
    """Calculate the SHA256 hash of a file."""
    h = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            h.update(chunk)
    
    return h.hexdigest()