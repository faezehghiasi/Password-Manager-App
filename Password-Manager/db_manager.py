"""Data‑layer: encrypt/decrypt & persistent storage (JSON)."""
import json
from pathlib import Path
from typing import List, Tuple

cipher = None            
current_owner = None     
_PASS_FILE = Path('passwords.json')

def _load_store() -> dict:
    if _PASS_FILE.exists():
        try:
            return json.loads(_PASS_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}

def _save_store(store: dict):
    _PASS_FILE.write_text(json.dumps(store, indent=2))

def set_cipher(c):
    global cipher
    cipher = c

def set_owner(owner: str):
    global current_owner
    current_owner = owner

def encrypt(text: str) -> str:
    if cipher is None:
        raise RuntimeError('Cipher not initialised')
    return cipher.encrypt(text.encode()).decode()

def decrypt_password(token: str) -> str:
    if cipher is None:
        raise RuntimeError('Cipher not initialised')
    return cipher.decrypt(token.encode()).decode()

def save_password(website: str, username: str, plain_password: str):
    """Encrypt and store password for the currently logged‑in user."""
    if cipher is None or current_owner is None:
        raise RuntimeError('Not logged in')
    store = _load_store()
    user_list = store.setdefault(current_owner, [])
    user_list.append({
        'website': website,
        'username': username,
        'password': encrypt(plain_password)
    })
    _save_store(store)

def get_all_passwords() -> List[Tuple[int, str, str, str]]:
    """Return [(idx, website, username, enc_pass), ...] for logged‑in user."""
    if current_owner is None:
        return []
    store = _load_store()
    rows = store.get(current_owner, [])
    result = []
    for i, item in enumerate(rows, 1):
        result.append((i, item['website'], item['username'], item['password']))
    return result
