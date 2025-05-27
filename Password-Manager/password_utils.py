import os
import hashlib

def generate_salt() -> bytes:
    return os.urandom(16)

def hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000).hex()
