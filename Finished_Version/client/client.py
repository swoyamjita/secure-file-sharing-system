# ===========================================================
#  Secure File Sharing Client (Final Version)
#  Author: Samikshya Swoyamjita
#  Version: 1.0 (Final Submission)
#  Date: 9 November 2025
# ===========================================================

import socket
import os
import hashlib
from tqdm import tqdm
import sys

# Dynamically add the parent directory (Finished_Version) to Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
    

from utils.config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE
from utils.encryption import load_or_create_key

# ===========================================================
#  Encryption Setup
# ===========================================================
fernet = load_or_create_key()

# ===========================================================
#  Authentication
# ===========================================================
username = input("Enter username: ")
password = input("Enter password: ")

s = socket.socket()
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(f"[!] Connection failed: {e}")
    exit()

# Send credentials to server
s.send(f"{username}|{password}".encode())
auth_status = s.recv(1024).decode()

if auth_status != "AUTH_SUCCESS":
    print("[!] Authentication failed. Connection closed.")
    s.close()
    exit()
else:
    print("[✓] Authentication successful. Secure channel established.\n")

# ===========================================================
#  File Selection & Validation
# ===========================================================
filename = input("Enter filename to send (from 'client/uploads/'): ")
filepath = os.path.join("client/uploads", filename)

if not os.path.exists(filepath):
    print(f"[!] File '{filename}' not found in client/uploads/")
    s.close()
    exit()

filesize = os.path.getsize(filepath)
print(f"[i] Preparing to send '{filename}' ({filesize} bytes) securely...")

# Send filename and filesize to server
s.send(f"{filename}|{filesize}".encode())

# ===========================================================
#  Secure File Transfer with Progress Bar
# ===========================================================
progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filepath, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        encrypted = fernet.encrypt(bytes_read)
        s.sendall(encrypted)
        progress.update(len(bytes_read))

progress.close()
print(f"[✓] File '{filename}' sent securely.")

# ===========================================================
#  Server Confirmation
# ===========================================================
confirmation = s.recv(1024).decode()
if confirmation == "UPLOAD_COMPLETE":
    print("[✓] Server confirmed upload completion.\n")
else:
    print("[!] Server did not confirm upload.")

# ===========================================================
#  Close Connection
# ===========================================================
s.close()
print("[✔] Connection closed. Operation complete.")
