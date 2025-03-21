# db_manager.py
import sqlite3
import base64
import os
import hashlib
from cryptography.fernet import Fernet

DB_FILE = "passwords.db"

FERNET_KEY = b'j-8L4YnHTJqCIWBCeVaJV54N-t5C8-j66n25_Me_Y98='
cipher = Fernet(FERNET_KEY)

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
    except Exception as e:
        print("Error initializing database:", e)
    finally:
        conn.close()

def save_password(website, username, password):
    try:
        enc_password = cipher.encrypt(password.encode()).decode()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                       (website, username, enc_password))
        conn.commit()
    except Exception as e:
        print("Error saving password:", e)
    finally:
        conn.close()

def get_all_passwords():
    rows = []
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords")
        rows = cursor.fetchall()
    except Exception as e:
        print("Error retrieving passwords:", e)
    finally:
        conn.close()
    return rows

def decrypt_password(enc_password: str) -> str:
    try:
        return cipher.decrypt(enc_password.encode()).decode()
    except Exception as e:
        print("Error decrypting password:", e)
        return "ERROR"
