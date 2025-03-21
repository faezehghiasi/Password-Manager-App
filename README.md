# 🔐 Password Manager (Python + Tkinter + SQLite)

A secure and user-friendly password manager with encryption and authentication, built using Python.

---

## ✨ Features

- **User Authentication** (Registration, Login, PBKDF2 Hashing, Brute-force Protection)
- **Password Management** (Generate, Encrypt, Store, View, Copy to Clipboard)
- **Security** (Fernet Encryption, Salted Hashing, No Plain-text Storage)

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.9 or newer
- `pip` package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/faezehghiasi/Password-Manager-App.git
   cd Password-Manager-App/password-manager
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Deactivate virtual environment (when done)**
   ```bash
   deactivate
   ```

---


## ⚠️ Security Notes

- **Encryption Key** (`FERNET_KEY`) should be stored securely (not hardcoded).
- **Credentials** are hashed before storage, but a database-based approach is better.
- **Login Attempts** are tracked in memory and reset upon restart.

---

## ✅ Future Improvements

- Master Password / Biometric Unlock
- Search & Filter Saved Passwords
- Export/Import Encrypted Backups
- Cloud Sync Support
- Dark Mode / Custom Themes


