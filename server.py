import socket
import threading
from OpenSSL import SSL

# List to keep track of connected clients
clients = []

# Create a socket and wrap it with SSL
def create_server_socket(port):
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('server.key')
    context.use_certificate_file('server.crt')
    
    server_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server_socket.bind(('192.168.122.1', port))
    server_socket.listen(5)
    return server_socket

def broadcast_message(message, sender_socket):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                clients.remove(client)  # Remove client if there's an error

def handle_client(client_socket):
    """Handle communication with a connected client."""
    clients.append(client_socket)  # Add the new client to the list
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            elif message.decode().lower() == 'bye':
                print(f"A client has disconnected.")
                break
            
            # Broadcast the received message to all other clients
            print(f'Client message: {message.decode()}')
            broadcast_message(message, client_socket)
    finally:
        client_socket.close()
        clients.remove(client_socket)  # Remove the client from the list when done
        print(f"Client disconnected.")

def start_server(port):
    """Start the server and accept incoming connections."""
    server_socket = create_server_socket(port)
    print(f"Server started on port {port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_server(8080)