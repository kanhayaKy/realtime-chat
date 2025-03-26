import sys
from select import select

from socket import socket, AF_INET, SOCK_STREAM
from constants import HOST, PORT


with socket(AF_INET, SOCK_STREAM) as client_sock:
    client_sock.connect((HOST, PORT))
    client_sock.setblocking(False)

    inputs = [client_sock, sys.stdin]
    outputs = []

    exit = False
    name = input("Name: ")
    print(f"{name}: ", end="", flush=True)

    while not exit:

        readable, writeable, exceptional = select(inputs, outputs, inputs)

        for source in readable:
            if source is client_sock:
                response = client_sock.recv(1024)
                print(f"Serv: {response.decode()}")
                print(f"{name}: ", end="", flush=True)

            else:
                message = sys.stdin.readline().strip()

                if message.lower() in ["quit", "exit"]:
                    exit = True
                else:
                    outputs.append(client_sock)

        for source in writeable:
            source.send(message.encode())
            outputs.remove(source)

    client_sock.close()
