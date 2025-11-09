# ===========================================================
#  User Management Utility (Add Users)
#  Author: Samikshya Swoyamjita
#  Date: 9 November 2025
# ===========================================================

import hashlib
import os

USERS_FILE = "server/users.txt"

def hash_password(password: str) -> str:
    """Return SHA256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username: str, password: str):
    """Add a new user to the users.txt file."""
    os.makedirs("server", exist_ok=True)

    # Create file if missing
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write("")

    # Check if username exists
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(username + ":"):
                print(f"[!] Username '{username}' already exists.")
                return

    # Add user
    hashed_pw = hash_password(password)
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{hashed_pw}\n")

    print(f"[✓] User '{username}' added successfully.")
    print(f"[i] Hashed password: {hashed_pw}")

if __name__ == "__main__":
    print("=== Add New User to Secure File Sharing System ===")
    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()

    if username and password:
        add_user(username, password)
    else:
        print("[!] Username and password cannot be empty.")
