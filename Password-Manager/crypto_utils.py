import base64
import hashlib
from cryptography.fernet import Fernet

def derive_key(password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return base64.urlsafe_b64encode(key)

def create_cipher(master_password: str, salt: bytes) -> Fernet:
    return Fernet(derive_key(master_password, salt))
