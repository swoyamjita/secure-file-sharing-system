# Day5 Security - server side
import socket
import threading
import os
import hashlib
from cryptography.fernet import Fernet

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5003
BUFFER_SIZE = 4096

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)

users = {}
if os.path.exists("users.txt"):
    with open("users.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                username, hashed_pw = line.split(":", 1)
                users[username.strip()] = hashed_pw.strip()

print("[DEBUG] Loaded users:")
for u, h in users.items():
    print(f"   -> {u} : {h}")
if not os.path.exists("uploads"):
    os.mkdir("uploads")

server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Secure Server listening on {SERVER_HOST}:{SERVER_PORT}")

def handle_client(client_socket, address):
    print(f"[+] Connection from {address}")

    auth_data = client_socket.recv(BUFFER_SIZE).decode()
    username, password = auth_data.split("|")
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    print(f"[DEBUG] Received -> username='{username}', password='{password}'")
    print(f"[DEBUG] Computed hash: {hashed_pw}")
    print(f"[DEBUG] Stored hash:   {users.get(username)}")

    if username in users and users[username] == hashed_pw:
        client_socket.send("AUTH_SUCCESS".encode())
        print(f"[✓] {username} authenticated successfully.")
    else:
        client_socket.send("AUTH_FAILED".encode())
        print(f"[!] Authentication failed for {username}")
        client_socket.close()
        return

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split("|")
    filesize = int(filesize)
    filepath = os.path.join("uploads", filename)

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

    print(f"[✓] Secure file '{filename}' received and decrypted successfully from {username}")
    client_socket.send("UPLOAD_COMPLETE".encode())
    client_socket.close()

while True:
    client_socket, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, address)).start()
