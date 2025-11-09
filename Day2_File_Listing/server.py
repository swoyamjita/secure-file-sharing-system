# Day2_File_Listing - server side
import socket
import os

HOST = '127.0.0.1'
PORT = 5050

SHARED_FOLDER = 'shared_files'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[*] Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"[+] Connected to client: {addr}")

    files = os.listdir(SHARED_FOLDER)
    if not files:
        file_list = "No files available."
    else:
        file_list = "\n".join(files)

    conn.send(file_list.encode())

    selected_file = conn.recv(1024).decode()
    print(f"[Client requested]: {selected_file}")

    conn.send(f"Server received your selection: {selected_file}".encode())

    conn.close()
    print("[*] Connection closed.\n")
