# Day5 Security - client side
import socket
import os
import hashlib
from tqdm import tqdm
from cryptography.fernet import Fernet

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5003
BUFFER_SIZE = 4096

with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

username = input("Enter username: ")
password = input("Enter password: ")

s = socket.socket()
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
s.connect((SERVER_HOST, SERVER_PORT))

s.send(f"{username}|{password}".encode())
auth_status = s.recv(1024).decode()

if auth_status != "AUTH_SUCCESS":
    print("[!] Authentication failed. Connection closed.")
    s.close()
    exit()
else:
    print("[✓] Authentication successful. Secure channel established.")

filename = input("Enter filename to send: ")
filepath = os.path.join("test_files", filename)

if not os.path.exists(filepath):
    print("File not found!")
    s.close()
    exit()

filesize = os.path.getsize(filepath)
s.send(f"{filename}|{filesize}".encode())

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
confirmation = s.recv(1024).decode()
if confirmation == "UPLOAD_COMPLETE":
    print("[✓] Server confirmed upload completion.")
s.close()
