# End-to-End Encrypted Chat Application

## Overview

This is a secure, end-to-end encrypted chat application built using Python, OpenSSL, and Tkinter for the user interface. The application ensures secure messaging through encryption, allowing only the sender and recipient to access the messages.

## Features

- **End-to-End Encryption**: Messages are encrypted using OpenSSL, ensuring they remain confidential between the sender and recipient.
- **Desktop Interface**: Built with Tkinter, providing a user-friendly desktop GUI.
- **Python-Powered**: Python enables secure and efficient communication through dedicated client and server scripts.

## Technology Stack

- **Programming Language**: Python
- **Encryption**: OpenSSL for secure message encryption and decryption
- **GUI**: Tkinter

## File Structure

The project includes the following files:

1. **`server.py`**: Handles message encryption, decryption, and relays messages to connected clients. This script must be run on the server side.
2. **`client.py`**: Represents the client interface for users. This script allows clients to connect to the server, send encrypted messages, and receive decrypted responses.
3. **Encryption Files**:
   - **Private Key** (`private.key`): Generated using OpenSSL and used to decrypt incoming messages.
   - **Certificate Signing Request (CSR)** (`server.csr`): Contains the certificate request.
   - **Self-Signed Certificate** (`selfsigned.crt`): Certifies authenticity and secures encryption.

## Installation

### Prerequisites
- **Python** (3.7 or higher)
- **OpenSSL**

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Jerry-britto/EncryptedChatApp.git
   cd EncryptedChatApp
   ```

2. **Install Dependencies**
   - Install dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Generate Encryption Keys and Certificates**
   - Run the following OpenSSL commands to create the necessary encryption files:
     ```bash
     openssl genpkey -algorithm RSA -out private.key
     openssl req -new -key private.key -out server.csr
     openssl req -x509 -key private.key -in server.csr -out selfsigned.crt -days 365
     ```

### Running the Application

1. **Start the Server**
   - Run `server.py` to start the server:
     ```bash
     python server.py
     ```

2. **Start a Client**
   - In a new terminal, run `client.py` to start a client session:
     ```bash
     python client.py
     ```
   - Multiple clients can connect to the server simultaneously, each communicating through encrypted channels.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with any improvements or new features.

