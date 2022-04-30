# Ex 4.4 - HTTP Server Shell
# Design Author: Barak Gonen
# Implementation Author: Tomer Yehezqel
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import os
import socket

# TO DO: set constants
LOCALHOST = '127.0.0.1'
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000
PROJECT_ROOT_DIR = os.getcwd()
WEB_ROOT_DIR = os.path.join(PROJECT_ROOT_DIR, 'webroot', 'webroot')
FIXED_RESPONSE = ''
DEFAULT_URL = os.path.join(WEB_ROOT_DIR, 'index.html').replace('\\',  '/')


def get_file_data(filename):
    """ Get data from file """
    filename_path = os.path.join(WEB_ROOT_DIR, filename[1:]).replace('\\',  '/')

    with open(filename_path, "r", encoding='utf-8') as file:
        file_data = file.read()
    return file_data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response

    if resource == '/':
        url = '/' + DEFAULT_URL.split('/')[-1]
    else:
        url = resource

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    # if url in REDIRECTION_DICTIONARY:
    # TO DO: send 302 redirection response

    # TO DO: extract requested file tupe from URL (html, jpg etc)
    filetype = url.split('.')[-1]
    if filetype == 'html':
        http_header = 'Accept: text/html\r\n'  # TO DO: generate proper HTTP header
    """
    elif filetype == 'jpg':
        http_header =  # TO DO: generate proper jpg header
    # TO DO: handle all other headers
    """

    # TO DO: read the data from the file
    data = get_file_data(url)
    # http_response = http_header + data
    http_response = data
    client_socket.send(http_response.encode())


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    request_parts = request.split()
    if (request_parts[0] == 'GET') and (request_parts[2] == 'HTTP/1.1') and (request[-2:] == '\r\n'):
        return True, request_parts[1]
    return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    client_socket.send(FIXED_RESPONSE.encode())

    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print(f'Got a valid HTTP request: {resource}')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
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
    # Call the main handler function
    main()
