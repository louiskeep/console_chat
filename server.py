import socket
import threading
import server_auth
from user import User

host = 'localhost'
port = 3434

# ipv4 / tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List of connected clients in chat
clients = []


def broadcast(message, source):
    # Broadcast message to chat room
    for client in clients:
        if client != source:
            try:
                client.send(message)
            except ConnectionResetError:
                continue

def handle(client):
    # Handle client communication
    while True:
        try:
            message = client.recv(1024)
            if message == (b'/login_request'):  # check if message is a log in request
                message = client.recv(1024)
                message = message.decode('utf-8').split(' ')
                username, password = message

                ans = str(server_auth.check_login(username, password))

                client.send(ans.encode('utf-8'))

            elif message == (b'/register_request'):  # check if message is a register request
                message = client.recv(1024)
                message = message.decode('utf-8').split(' ')
                username, password = message
                ans = str(server_auth.check_register(username, password))
                client.send(ans.encode('utf-8'))

            else:
                broadcast(message, client)

        except ConnectionResetError:
            clients.remove(client)
            broadcast(f"{client} has left the chat.".encode('utf-8'), client)
            break


def receive():
    # Receive client connection and add to client list
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Listening")
receive()