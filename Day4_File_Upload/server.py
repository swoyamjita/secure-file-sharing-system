# Day4 File Upload - server side
import socket
import threading
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
BUFFER_SIZE = 4096

if not os.path.exists("uploads"):
    os.mkdir("uploads")

server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Server listening as {SERVER_HOST}:{SERVER_PORT}")

def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    try:
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split("|")
        filesize = int(filesize)

        filepath = os.path.join("uploads", filename)
        print(f"[+] Receiving {filename} ({filesize} bytes) from {address}")

        with open(filepath, "wb") as f:
            total_received = 0
            while total_received < filesize:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                total_received += len(bytes_read)

        print(f"[✓] File '{filename}' received successfully from {address}")
    except Exception as e:
        print(f"[!] Error with {address}: {e}")
    finally:
        client_socket.close()

while True:
    client_socket, address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()
