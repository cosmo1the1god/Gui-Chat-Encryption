import queue
import threading
import socket
import base64

# Key to decrypt messages from clients and encrypt messages to clients
messages = queue.Queue()
clients = []
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 9999))

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
            message_bytes = base64.b64decode(message)
            message = message_bytes.decode('utf-8', 'ascii')
            print(message)
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.startswith("SIGNUP_TAG:"):
                        name = message[message.index(":") + 1:]
                        server_socket.sendto(f"Welcome {name}!".encode(), client)
                    else:
                        server_socket.sendto(message.encode(), client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
