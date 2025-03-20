from socket import socket, AF_INET, SOCK_STREAM
from constants import HOST, PORT


with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((HOST, PORT))

    while True:
        message = input("Send: ")

        if message.lower() in ["quit", "exit"]:
            break

        client_sock.send(message.encode())

        response = client_sock.recv(1024)
        print(f"Recv: {response.decode()}")

    client_sock.close()
