import os
import pathlib

LOCALHOST = '127.0.0.1'
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000  # _MS
WEB_ROOT_DIR = 'webroot'
DEFAULT_URL = (pathlib.Path(WEB_ROOT_DIR) / 'index.html').as_posix()
CONTENT_TYPE_HEADER = {'html': 'text/html; charset=utf-8',
                       'txt': 'text/html; charset=utf-8',
                       'jpg': 'image/jpeg',
                       'gif': 'image/gif',
                       'js': 'text/javascript; charset=UTF-8',
                       'css': 'text/css',
                       'ico': 'image/x-icon'}


def get_file_data(filename):
    """ Get data from file """
    filename_path = pathlib.Path(WEB_ROOT_DIR + filename)
    if filename_path.is_file():
        with open(filename_path, "rb") as file:
            file_data = file.read()
            return True, file_data
    else:
        return False, "404 Not Found"


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""

    if resource == '/':
        url = '/' + pathlib.Path(DEFAULT_URL).name
    else:
        url = resource

    resource_type = ''
    if '.' in url:
        resource_type = 'file'
    elif '?' in url:
        resource_type = 'parameter'

    # extract requested file type from URL (html, jpg etc):
    data = None
    content_type = 0
    get_data_status = False
    if resource_type == 'file':
        filetype = url.split('.')[-1]
        content_type = CONTENT_TYPE_HEADER[filetype]
        # read the data from the file:
        get_data_status, data = get_file_data(url)

    # Handle parameter request:
    elif resource_type == 'parameter':
        parameter_type = url.split('?')[0]
        parameter_value = url.split('?')[1]
        if parameter_type[1:] == 'calculate-next':
            number = parameter_value.split('=')[1]
            content_type = CONTENT_TYPE_HEADER['txt']
            data = str(int(number) + 1).encode()
            get_data_status = True
        else:
            print(f'Unknown parameter type: {parameter_type[1:]}')
            get_data_status = False

    # sending the data with proper message:
    if content_type:
        http_response = f"HTTP/1.1 200 OK\r\n Content-Length: {len(data)}\r\n Content-Type: {content_type}\r\n\r\n".encode()
        http_response += data
    else:
        print(f"False http header is received: {content_type}.")
        http_response = f"HTTP/1.1 403 Forbidden\r\n".encode()
        http_response += data

    if get_data_status:
        client_socket.send(http_response)
    else:
        http_response = f"HTTP/1.1 {data}\r\n\r\n"
        client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    request_parts = request.split()
    if (request_parts[0], request_parts[2], request[-2:]) == ('GET', 'HTTP/1.1', '\r\n'):
        return True, request_parts
    return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

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
