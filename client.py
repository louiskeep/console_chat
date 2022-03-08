import socket
import threading
from client_auth import ClientAuth

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 3434))


def receive():
    # Receiving chat messages
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)

        except Exception as e:
            print(e)
            client.close()
            break


def write(username):
    # Writing chat messages
    while True:
        #print(username + ': ', end='')
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))


if __name__ == '__main__':
    client_auth = ClientAuth()
    # returns client username input from terminal and verification bool from login
    try:
        username, access = client_auth.welcome()
    except ConnectionResetError as e:
        print("Server connection severed.")
        print(e)

    if access:
        print("Welcome to chat!")
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write, args=(username,))
        write_thread.start()
    else:
        print("Unable to verify.")