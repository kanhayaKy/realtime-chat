from socket import socket, AF_INET, SOCK_STREAM
import threading

from constants import HOST, PORT

clients = set()


def handle_connection(connection, address):
    try:
        print(f"Recvd connection from {address}")
        while True:
            request_data = connection.recv(1024).decode("utf-8")
            if not request_data:
                break

            print(f"Data from {address}: {request_data}")
            response = request_data.encode()

            for client in clients:
                if client is not connection:
                    client.send(response)
    except Exception as err:
        print(f"Error occured handling connection {address} {err}")
    finally:
        connection.close()
        clients.remove(connection)


with socket(AF_INET, SOCK_STREAM) as server_socket:
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on port {PORT}...")
        while True:
            connection, address = server_socket.accept()
            clients.add(connection)

            client_thread = threading.Thread(
                target=handle_connection, args=(connection, address), daemon=True
            )
            client_thread.start()
    except Exception as e:
        print(f"error occured ... {e}")
    finally:
        server_socket.close()
