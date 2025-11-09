# utils/encryption.py

from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_or_create_key():
    """Load the encryption key from KEY_FILE or create it if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)
