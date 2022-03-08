class User:

    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = username
