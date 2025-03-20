from socket import socket, AF_INET, SOCK_STREAM

from constants import HOST, PORT


def handle_connection(connection, address):
    try:
        print(f"Recvd connection from {address}")
        while True:
            request_data = connection.recv(1024).decode("utf-8")
            if not request_data:
                break

            print(f"Data from {address}: {request_data}")
            connection.send(request_data.encode())
    except Exception as err:
        print(f"Error occured handling connection {address} {err}")
    finally:
        connection.close()


with socket(AF_INET, SOCK_STREAM) as server_socket:
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on port {PORT}...")
        while True:
            connection, address = server_socket.accept()
            handle_connection(connection, address)
    except Exception as e:
        print(f"error occured ... {e}")
    finally:
        server_socket.close()
