import socket
import threading
from OpenSSL import SSL

# Dictionary to keep track of connected clients in different chat rooms
chat_rooms = {}

# Create a socket and wrap it with SSL
def create_server_socket(port):
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('server.key')
    context.use_certificate_file('server.crt')
    
    server_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    return server_socket

def broadcast_message(message, sender_socket, room_id):
    """Send a message to all connected clients in the specified room except the sender."""
    for client in chat_rooms[room_id]:
        if client != sender_socket:
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                chat_rooms[room_id].remove(client)  # Remove client if there's an error

def handle_client(client_socket):
    """Handle communication with a connected client."""
    room_id = None
    
    try:
        # Prompt the client to choose a chat room
        while True:
            client_socket.sendall(b"Available chat rooms:\n")
            for room in chat_rooms.keys():
                client_socket.sendall(f"Chat ID: {room}\n".encode())
            client_socket.sendall(b"Enter the Chat ID you want to join or type 'new' to create a new room: ")
            
            choice = client_socket.recv(1024).decode().strip()
            if choice.lower() == 'new':
                room_id = str(len(chat_rooms) + 1)  # Create new room with an incremental ID
                chat_rooms[room_id] = []
                break
            elif choice in chat_rooms:
                room_id = choice
                break
            else:
                client_socket.sendall(b"Invalid choice. Please try again.\n")

        # Add the new client to the selected chat room
        chat_rooms[room_id].append(client_socket)
        print(f"Client joined room {room_id}")

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            elif message.decode().lower() == 'bye':
                print(f"A client has disconnected from room {room_id}.")
                break
            
            # Broadcast the received message to all other clients in the same room
            print(f'Client message in room {room_id}: {message.decode()}')
            broadcast_message(message, client_socket, room_id)
    finally:
        if room_id and client_socket in chat_rooms[room_id]:
            chat_rooms[room_id].remove(client_socket)  # Remove the client from the list when done
            
            # Check if the room is empty and remove it if so
            if not chat_rooms[room_id]:  # If no clients left in the room
                del chat_rooms[room_id]  # Delete the chat room
                print(f"Chat room {room_id} has been deleted as it is empty.")
                
        client_socket.close()
        print(f"Client disconnected from room {room_id}.")

def start_server(port):
    """Start the server and accept incoming connections."""
    server_socket = create_server_socket(port)
    print(f"Server started on port {port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_server(8000)