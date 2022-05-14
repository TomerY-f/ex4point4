"""
Ex 4.4 - HTTP Server Shell
Design Author: Barak Gonen
Implementation Author: Tomer Yehezqel
Purpose: Provide a basis for Ex. 4.4
Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
Usage: Fill the missing functions and constants
"""

import socket

from client_handler import handle_client

LOCALHOST = '127.0.0.1'
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000  # _MS


def main():
    # Open a socket and loop forever while waiting for clients:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LOCALHOST, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)
        continue


if __name__ == "__main__":
    main()
