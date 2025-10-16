"""
Testes para hashing.sha256_bytes e cache
"""
import pytest
from core.hashing import sha256_bytes, load_hash_cache, save_hash_cache

def test_sha256_bytes():
    data = b"teste"
    h = sha256_bytes(data)
    assert len(h) == 64
    assert isinstance(h, str)

def test_cache(tmp_path):
    hashes = {"abc", "def"}
    save_hash_cache(hashes)
    loaded = load_hash_cache()
    assert hashes == loaded
