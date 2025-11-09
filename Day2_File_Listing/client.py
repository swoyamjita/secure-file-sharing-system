# Day2_File_Listing - client side
import socket

HOST = '127.0.0.1'
PORT = 5050

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

file_list = client_socket.recv(4096).decode()
print("Available files on server:\n")
print(file_list)

if "No files available" not in file_list:
    filename = input("\nEnter the name of the file you want to download: ")
    client_socket.send(filename.encode())

    response = client_socket.recv(1024).decode()
    print(f"\n[Server]: {response}")
else:
    print("\nNo files to select.")

client_socket.close()
