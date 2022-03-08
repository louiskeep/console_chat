import socket
from getpass import getpass
import sys
from Validate import Validate


class ClientAuth:

    def __init__(self):
        print("Connecting to server...")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 3434))
        self.username = ""

    def welcome(self):
        # Entrance message
        while True:
            action = input("Select option:\n1. Login \n2. Register\n")
            print()

            # Login
            if action == '1':
                username, login_bool = self.login()
                if login_bool == 'True':
                    return username, True

                else:
                    print("Invalid login credentials.")
                    continue

            # Register
            if action == '2':
                response = self.register()
                if response == '/user registered':
                    # user was registered in system
                    print()  # Spacer
                    print("You're registered! Please log in.")

                elif response == '/user already exists':
                    print("User already exists!\nChoose another name or return to log in.")

                else:
                    print(f"Something went wrong: {response}")

    def login(self):
        # Username handling
        self.username = input("Username: ").lower()

        # Handling for password input on all terminals
        if not sys.stdin.isatty():
            # Exposed terminal
            print("Your terminal is insecure for password input.\n*** WARNING: PASSWORD IS VISIBLE IN TERMINAL ***")
            password = input("Password: ")
            print()
        else:
            # Secure terminal
            password = getpass()

        # send data to server
        self.client.send('/login_request'.encode('utf-8'))
        self.client.send(f'{self.username} {password}'.encode('utf-8'))
        access = self.client.recv(1024).decode('utf-8')

        # Return username and login verification
        return self.username, access

    def register(self):
        while True:
            username = input("Username: ").lower()
            validate_username = Validate(username)
            if validate_username.validate_username():
                break
            else:
                print("Usernames cannot contain the following characters: ' ;,?'")

        self.username = username

        # Handling for password input on all terminals
        if not sys.stdin.isatty():
            # Exposed terminal
            print("Your terminal is insecure for password input.\n*** WARNING: PASSWORD IS VISIBLE IN TERMINAL ***")
            while True:
                password = input("Password: ")
                validate_password = Validate(password)
                if validate_password.validate_password():
                    break
                else:
                    print("Passwords must contain: upper case letter, lowercase letter, "
                          "digit and a symbol of: !@#$%^&*()")
        else:
            # Secure terminal
            while True:
                password = getpass()
                validate_password = Validate(password)
                if validate_password.validate_password():
                    break
                else:
                    print("Passwords must contain: upper case letter, lowercase letter, "
                          "digit and a symbol of: !@#$%^&*()")

        # send data to server
        self.client.send('/register_request'.encode('utf-8'))
        self.client.send(f'{self.username} {password}'.encode('utf-8'))
        register_response = self.client.recv(1024).decode('utf-8')
        return register_response