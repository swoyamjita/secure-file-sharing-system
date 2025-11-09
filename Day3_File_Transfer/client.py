import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001
BUFFER_SIZE = 4096

filename = "sample.txt"
filesize = os.path.getsize(filename)

# Create socket
s = socket.socket()
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# Send filename first
s.send(filename.encode())

# Send file content
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # File transmitting is done
            break
        s.sendall(bytes_read)

print(f"[+] File '{filename}' sent successfully.")
s.close()
