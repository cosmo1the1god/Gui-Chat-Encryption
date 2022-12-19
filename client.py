import socket
import threading
import random
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import simpledialog
import base64
from cryptography.fernet import Fernet


# Chat window with input field and send button and text from another user

class Client:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(("localhost", random.randint(8000, 9000)))

        msg = tk.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        if self.nickname is None:
            self.nickname = "Anonymous"

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)

        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tk.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tk.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkst.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tk.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def receive(self):
        while self.running:
            try:
                try:
                    message, _ = self.client.recvfrom(1024)
                    message = message.decode('utf-8')
                    if message == "NICK":
                        self.client.send(self.nickname.encode('utf-8'))
                    else:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
                except ConnectionError:
                    pass
            except:
                print("An error occurred!")
                self.client.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.client.close()
        exit(0)

    # write on the chat window
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        with open("key.mp", "rb") as file:
            key = file.read()

        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())
        self.client.sendto(encMessage, ("localhost", 9999))
        self.input_area.delete('1.0', 'end')


# Start the chat window
client = Client()
