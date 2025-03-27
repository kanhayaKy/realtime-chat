import sys
from select import select

from socket import socket, AF_INET, SOCK_STREAM
from constants import HOST, PORT


with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((HOST, PORT))
    client_sock.setblocking(False)
    print(f"Connected to {HOST}:{PORT}")

    inputs = [client_sock, sys.stdin]
    outputs = []

    exit = False
    name = input("Name: ")
    print("-------------------")
    print(f"Welcome {name}!!")
    print("-------------------")

    while not exit:

        readable, writeable, exceptional = select(inputs, outputs, inputs)

        for source in readable:
            if source is client_sock:
                response = client_sock.recv(1024)
                print(response.decode())

            else:
                message = sys.stdin.readline().strip()

                if message.lower() in ["quit", "exit"]:
                    exit = True
                else:
                    message = f"{name}: {message}"
                    outputs.append(client_sock)

        for source in writeable:
            source.send(message.encode())
            outputs.remove(source)

    client_sock.close()
