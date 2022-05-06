"""
Ex 4.4 - HTTP Server Shell
Design Author: Barak Gonen
Implementation Author: Tomer Yehezqel
Purpose: Provide a basis for Ex. 4.4
Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
Usage: Fill the missing functions and constants
"""

import os
import socket

LOCALHOST = '127.0.0.1'
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000
PROJECT_ROOT_DIR = os.getcwd()
WEB_ROOT_DIR = os.path.join(PROJECT_ROOT_DIR, 'webroot', 'webroot')
FIXED_RESPONSE = ''
DEFAULT_URL = os.path.join(WEB_ROOT_DIR, 'index.html').replace('\\', '/')


def get_file_data(filename):
    """ Get data from file """
    filename_path = os.path.join(WEB_ROOT_DIR, filename[1:]).replace('\\', '/')
    try:
        with open(filename_path, "rb") as file:
            file_data = file.read()
            return True, file_data
    except FileNotFoundError:
        file_not_found_log = "404 Not Found"
        return False, file_not_found_log


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""

    if resource == '/':
        url = '/' + DEFAULT_URL.split('/')[-1]
    else:
        url = resource

    # extract requested file type from URL (html, jpg etc):
    filetype = url.split('.')[-1]
    content_type = 0
    if (filetype == 'html') or (filetype == 'txt'):
        content_type = 'text/html; charset=utf-8'
    elif filetype == 'jpg':
        content_type = 'image/jpeg'
    elif filetype == 'js':
        content_type = 'text/javascript; charset=UTF-8'
    elif filetype == 'css':
        content_type = 'text/css'
    elif filetype == 'ico':
        content_type = 'image/x-icon'

    # read the data from the file:
    get_file_validation_flag, data = get_file_data(url)
    data_length = len(data)

    # sending the data with proper message:
    if content_type:
        http_response = f"HTTP/1.1 200 OK\r\n Content-Length: {data_length}\r\n Content-Type: {content_type}\r\n\r\n".encode()
        http_response += data
    else:
        print(f"False http header is received: {content_type}.")
        http_response = f"HTTP/1.1 403 Forbidden\r\n".encode()
        http_response += data
    if get_file_validation_flag:
        client_socket.send(http_response)
    else:
        http_response = f"HTTP/1.1 {data}\r\n\r\n"
        client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    request_parts = request.split()
    if (request_parts[0] == 'GET') and (request_parts[2] == 'HTTP/1.1') and (request[-2:] == '\r\n'):
        return True, request_parts
    return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    client_socket.send(FIXED_RESPONSE.encode())

    while True:
        client_request = client_socket.recv(1024).decode()
        valid_http, request_parts = validate_http_request(client_request)
        if valid_http:
            resource = request_parts[1]
            print(f'Got a valid HTTP request: {resource}')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


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
