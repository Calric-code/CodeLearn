import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

# Function to receive messages
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
        except:
            break

# Function to send a message
def send_message():
    message = message_entry.get()
    if message:
        client.send(message.encode("utf-8"))
        message_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Chatroom")

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=15)
chat_box.pack(pady=5)

message_entry = tk.Entry(root, width=40)
message_entry.pack(pady=5, side=tk.LEFT)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5)

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start receiving messages in a thread
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
