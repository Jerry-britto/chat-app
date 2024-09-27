import socket
from OpenSSL import SSL
import threading

def create_client_socket(server_ip, port):
    context = SSL.Context(SSL.SSLv23_METHOD)
    client_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    client_socket.connect((server_ip, port))
    return client_socket

def send_message(client_socket):
    while True:
        message = input("Enter message: ")
        client_socket.send(message.encode())
        if message.lower() == 'bye':
            print("You have disconnected from the chat.")
            break  # Exit loop when 'bye' is sent

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break  # Break if connection is closed
            print(f"Received: {message.decode()}")
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit on error

def start_client(server_ip, port):
    client_socket = create_client_socket(server_ip, port)
    
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    
    send_message(client_socket)
    
    # Close the socket after sending 'bye'
    client_socket.close()

start_client('192.168.122.1', 8080)