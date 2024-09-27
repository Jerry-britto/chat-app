import socket
import threading
import rsa

choice = input("Do you want to host(1) or connect(2)")

if choice == '1':

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",8000))
    server.listen()

    client,_ = server.accept()

elif choice == '2':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('127.0.0.1',8000))
else:
    exit()

def send_messages(client):
    while True:
        message = input("")
        client.send(message.encode())
        print("You ",message)
        if message.lower() == 'bye':
            exit()

def receive_messages(client):
    while True:
        message = client.recv(1024).decode()
        print("Partner ", message)
        if message == 'bye':
            exit()

threading.Thread(target=send_messages,args=(client,)).start()
threading.Thread(target=receive_messages,args=(client,)).start()

