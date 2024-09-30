import socket
from OpenSSL import SSL
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, server_ip, port):
        self.client_socket = self.create_client_socket(server_ip, port)
        
        # Set up the GUI
        self.window = tk.Tk()
        self.window.title("Chat Client")
        
        self.chat_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10)
        
        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack(padx=0, pady=10)
        self.message_entry.bind("<Return>", self.send_message)  # Send message on Enter key
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close
        
        # Start the thread to receive messages
        threading.Thread(target=self.receive_messages, daemon=True).start()
        
        self.window.mainloop()

    def create_client_socket(self, server_ip, port):
        context = SSL.Context(SSL.SSLv23_METHOD)
        client_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        client_socket.connect((server_ip, port))
        return client_socket

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode())
            if message.lower() == 'bye':
                print("You have disconnected from the chat.")
                self.on_closing()  # Close the app if 'bye' is sent
            else:
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, f"You: {message}\n")
                self.chat_area.config(state='disabled')
                self.message_entry.delete(0, tk.END)  # Clear the entry box

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if not message:
                    break  # Break if connection is closed
                decoded_message = message.decode()
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, f"Received: {decoded_message}\n")
                self.chat_area.config(state='disabled')
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit on error

    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client_socket.close()
            self.window.destroy()

if __name__ == "__main__":
    ChatClient('172.16.128.25', 8080)