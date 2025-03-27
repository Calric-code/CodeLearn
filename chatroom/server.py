import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []
server_running = True
lock = threading.Lock()  # Add a lock for thread-safe operations

def handle_client(client_socket):
    global server_running
    while server_running:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Received: {message}")
            broadcast(message, client_socket)
        except (ConnectionResetError, OSError):
            break
    # Remove client after disconnection
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode("utf-8"))
                except (ConnectionResetError, OSError):
                    # Remove client if sending fails
                    if client in clients:
                        clients.remove(client)

def start_server():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server running on {HOST}:{PORT}")

    try:
        while server_running:
            try:
                client_socket, addr = server.accept()
                print(f"New connection from {addr}")
                with lock:
                    clients.append(client_socket)
                threading.Thread(target=handle_client, args=(client_socket,)).start()
            except OSError:
                break
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_running = False
        # Close all client connections
        with lock:
            for client in clients:
                client.close()
            clients.clear()
        server.close()
        print("Server shut down.")

start_server()

