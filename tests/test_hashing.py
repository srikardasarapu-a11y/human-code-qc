import os
import tempfile
import hashlib
import pytest

from src.human_code_qc.hashing import hash_bytes, hash_text, hash_file
from src.human_code_qc.manifests.verifier import verify_archive_integrity, IntegrityError

def test_sha256_known_byte():
    # 1. SHA-256 known-byte test
    assert hash_bytes(b"hello") == hashlib.sha256(b"hello").hexdigest()
    assert hash_text("hello") == hashlib.sha256(b"hello").hexdigest()

def test_empty_file_hash():
    # 2. Empty file hash
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name
    try:
        expected = hashlib.sha256(b"").hexdigest()
        assert hash_file(path) == expected
    finally:
        os.remove(path)

def test_large_file_hash():
    # 3. Large file hash (streaming simulation)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        # Write 100KB in small chunks to ensure chunking works
        data = b"a" * 1024
        for _ in range(100):
            f.write(data)
        path = f.name
        
    try:
        expected = hashlib.sha256(b"a" * 1024 * 100).hexdigest()
        # use a very small chunk_size to force loop iterations
        assert hash_file(path, chunk_size=1024) == expected
    finally:
        os.remove(path)

def test_identical_and_different_files():
    # 4. Identical files and 5. Different files
    with tempfile.NamedTemporaryFile(delete=False) as f1, \
         tempfile.NamedTemporaryFile(delete=False) as f2, \
         tempfile.NamedTemporaryFile(delete=False) as f3:
        f1.write(b"data1")
        f2.write(b"data1")
        f3.write(b"data2")
        p1, p2, p3 = f1.name, f2.name, f3.name
        
    try:
        assert hash_file(p1) == hash_file(p2)
        assert hash_file(p1) != hash_file(p3)
    finally:
        os.remove(p1)
        os.remove(p2)
        os.remove(p3)

def test_deterministic_hashing():
    # 6. Deterministic hashing
    # Hash bytes repeatedly and ensure it remains the exact same string
    h1 = hash_text("deterministic")
    h2 = hash_text("deterministic")
    assert h1 == h2

def test_archive_integrity():
    # 12. Archive integrity match and 13. Archive integrity mismatch
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"fake_archive_data")
        path = f.name
        
    baseline = hash_file(path)
    
    try:
        # Match
        verify_archive_integrity(path, baseline)
        
        # Mismatch
        with pytest.raises(IntegrityError):
            verify_archive_integrity(path, "invalid_hash_value")
    finally:
        os.remove(path)
