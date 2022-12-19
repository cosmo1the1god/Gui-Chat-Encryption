import queue
import threading
import socket
from cryptography.fernet import Fernet

# Key to decrypt messages from clients and encrypt messages to clients
messages = queue.Queue()
clients = []
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 9999))

with open("key.mp", "rb") as file:
    key = file.read()

print("Server is running...")


def receive():
    while True:
        try:
            message, addr = server_socket.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass


def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            fernet = Fernet(key)
            dec_message = fernet.decrypt(message).decode()
            print(dec_message)
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if dec_message.startswith("SIGNUP_TAG:"):
                        name = dec_message[dec_message.index(":") + 1:]
                        server_socket.sendto(f"Welcome {name}!".encode(), client)
                    else:
                        server_socket.sendto(dec_message.encode(), client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
