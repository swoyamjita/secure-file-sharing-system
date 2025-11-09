# Day4 File Upload - client side
import socket
import os
from tqdm import tqdm   

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
BUFFER_SIZE = 4096

filename = input("Enter filename to send: ")
filepath = os.path.join("test_files", filename)

if not os.path.exists(filepath):
    print("File not found!")
    exit()

s = socket.socket()
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

filesize = os.path.getsize(filepath)
s.send(f"{filename}|{filesize}".encode())

progress = tqdm(
    range(filesize),
    f"Sending {filename}",
    unit="B",
    unit_scale=True,
    unit_divisor=1024
)

with open(filepath, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))

progress.close()
print(f"[✓] File '{filename}' sent successfully.")
s.close()
