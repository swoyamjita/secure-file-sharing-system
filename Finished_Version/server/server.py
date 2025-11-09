# ===========================================================
#  Secure File Sharing Server (Final Version)
#  Author: Samikshya Swoyamjita
#  Version: 1.0 (Final Submission)
#  Date: November 2025
# ===========================================================

import socket
import threading
import os
import hashlib
import datetime
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
#  Logging Utility
# ===========================================================
def log_event(message):
    """Append timestamped message to server/logs/activity.log."""
    log_dir = "server/logs"
    log_file = os.path.join(log_dir, "activity.log")

    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# ===========================================================
#  Load Users
# ===========================================================
users = {}
users_file = "server/users.txt"

if os.path.exists(users_file):
    with open(users_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                username, hashed_pw = line.split(":", 1)
                users[username.strip()] = hashed_pw.strip()

print("[DEBUG] Loaded users:")
for u, h in users.items():
    print(f"   -> {u} : {h}")

# ===========================================================
#  Server Directory Setup
# ===========================================================
UPLOAD_DIR = "server/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===========================================================
#  Start Server
# ===========================================================
server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Secure Server listening on {SERVER_HOST}:{SERVER_PORT}")
log_event("Server started and listening for connections.")

# ===========================================================
#  Handle Each Client
# ===========================================================
def handle_client(client_socket, address):
    print(f"[+] Connection from {address}")
    log_event(f"New connection from {address}")

    try:
        auth_data = client_socket.recv(BUFFER_SIZE).decode()
        username, password = auth_data.split("|")
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        print(f"[DEBUG] Received -> username={username}, hash={hashed_pw}, stored={users.get(username)}")

        if username in users and users[username] == hashed_pw:
            client_socket.send("AUTH_SUCCESS".encode())
            print(f"[✓] {username} authenticated successfully.")
            log_event(f"User '{username}' authenticated successfully from {address}")
        else:
            client_socket.send("AUTH_FAILED".encode())
            print(f"[!] Authentication failed for {username}")
            log_event(f"Failed authentication attempt for '{username}' from {address}")
            client_socket.close()
            return

        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split("|")
        filesize = int(filesize)
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            total = 0
            while total < filesize:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    decrypted = fernet.decrypt(data)
                    f.write(decrypted)
                except Exception:
                    pass
                total += len(data)

        print(f"[✓] File '{filename}' securely received and decrypted from {username}.")
        log_event(f"File '{filename}' uploaded successfully by '{username}'")

        client_socket.send("UPLOAD_COMPLETE".encode())
        client_socket.close()

    except Exception as e:
        print(f"[!] Error handling {address}: {e}")
        log_event(f"Error handling client {address}: {e}")
        client_socket.close()

# ===========================================================
#  Accept Connections (Main Loop)
# ===========================================================
try:
    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
except KeyboardInterrupt:
    print("\n[!] Server shutting down gracefully.")
    log_event("Server manually stopped by administrator.")
    server_socket.close()
