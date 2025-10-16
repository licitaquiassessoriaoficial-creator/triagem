"""
Funções de hash SHA-256 e cache de hashes
"""
import hashlib
import json
from pathlib import Path
from typing import Set

CACHE_PATH = Path(".odq_cache/hashes.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_hash_cache() -> Set[str]:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_hash_cache(hashes: Set[str]):
    CACHE_PATH.parent.mkdir(exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(list(hashes), f)
