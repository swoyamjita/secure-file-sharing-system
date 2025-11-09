import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001
BUFFER_SIZE = 4096

server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = server_socket.accept()
print(f"[+] {address} connected.")

filename = client_socket.recv(BUFFER_SIZE).decode()
print(f"[+] Receiving file: {filename}")

with open("received_" + filename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)

print(f"[+] File {filename} received successfully.")
client_socket.close()
server_socket.close()
