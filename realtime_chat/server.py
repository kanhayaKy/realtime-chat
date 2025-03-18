from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 7007


def handle_connection(connection, address):
    with connection:
        try:
            print(f"Recvd connection from {address}")
            request_data = connection.recv(1024).decode("utf-8")
            http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(request_data)}\r\n\r\n{request_data}"
            connection.send(http_response.encode())
        except Exception as err:
            print(f"Error occured handling connection {connection} {address}")


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
