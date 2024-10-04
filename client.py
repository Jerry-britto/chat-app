import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from OpenSSL import SSL

class ChatClient:
    def __init__(self, server_ip, port):
        self.client_socket = self.create_client_socket(server_ip, port)

        # Set up the GUI
        self.window = tk.Tk()
        self.window.title("Chat Client")
        self.window.geometry("400x500")
        self.window.configure(bg="#E5FFF7")

        self.chat_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.chat_frame.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

        self.chat_area = tk.Frame(self.chat_frame, bg="#f0f0f0")
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_area, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_area, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        self.message_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.message_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.message_entry = tk.Entry(self.message_frame, bg="#ffffff", font=("Arial", 12), bd=0, highlightthickness=0)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_message, bg="#007BFF", fg="#ffffff", font=("Arial", 10), bd=0)
        self.send_button.pack(side=tk.RIGHT)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind mouse wheel event for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Start the thread to receive messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.window.mainloop()

    def create_client_socket(self, server_ip, port):

        # with end to end encryption
        context = SSL.Context(SSL.SSLv23_METHOD)
        client_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        client_socket.connect((server_ip, port))
        return client_socket

        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.connect((server_ip, port))
        # return client_socket

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode())
            if message.lower() == 'bye':
                print("You have disconnected from the chat.")
                self.on_closing()
            else:
                self.display_message(f"{message}", "outgoing")
                self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if not message:
                    break
                decoded_message = message.decode()
                self.display_message(f"{decoded_message}", "incoming")
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def display_message(self, message, message_type):
        timestamp = datetime.now().strftime("%H:%M")
        bubble_color = "#e0f7e0" if message_type == "outgoing" else "#ffffff"
        text_color = "#007A33" if message_type == "outgoing" else "#000000"

        # Create a frame for each message
        frame = tk.Frame(self.inner_frame, bg="#f0f0f0")
        
        # Increased padding for outgoing messages
        bubble_padding = (15, 10) if message_type == "outgoing" else (10, 5)
        bubble = tk.Label(frame, text=message, bg=bubble_color, fg=text_color, font=("Arial", 12), bd=0, padx=bubble_padding[0], pady=bubble_padding[1], wraplength=250, justify="left")
        
        time_label = tk.Label(frame, text=timestamp, bg="#f0f0f0", fg="gray", font=("Arial", 8))

        # Adjust alignment
        if message_type == "incoming":
            bubble.pack(anchor='w', padx=(10, 50))  # Left-align with padding
            time_label.pack(anchor='w', padx=(10, 50))  # Align time label with the bubble
        else:
            bubble.pack(anchor='e', padx=(50, 10))  # Right-align with padding
            time_label.pack(anchor='e', padx=(50, 10))  # Align time label with the bubble

        frame.pack(pady=(5, 0), fill=tk.X)

        # Update the canvas
        self.inner_frame.update_idletasks()  # Update the inner frame before calculating the scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Configure scroll region
        self.canvas.yview_moveto(1)  # Auto-scroll to the bottom

    def on_mouse_wheel(self, event):
        # Scroll the canvas based on mouse wheel movement
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client_socket.close()
            self.window.destroy()

if __name__ == "__main__":
    ChatClient('192.168.122.1', 8000)
