import os

LOCALHOST = '127.0.0.1'
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1000  # _MS
WEB_ROOT_DIR = os.path.join('.', 'webroot')
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

    resource_type = ''
    if '.' in url:
        resource_type = 'file'
    elif '?' in url:
        resource_type = 'parameter'

    # extract requested file type from URL (html, jpg etc):
    data = None
    content_type = 0
    get_data_validation_flag = False
    if resource_type == 'file':
        filetype = url.split('.')[-1]
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
        get_data_validation_flag, data = get_file_data(url)

    # Handle parameter request:
    elif resource_type == 'parameter':
        parameter_type = url.split('?')[0]
        parameter_value = url.split('?')[1]
        if parameter_type[1:] == 'calculate-next':
            number = parameter_value.split('=')[1]
            content_type = 'text/html; charset=utf-8'
            data = str(int(number) + 1).encode()
            get_data_validation_flag = True
        else:
            print(f'Unknown parameter type: {parameter_type[1:]}')
            get_data_validation_flag = False

    data_length = len(data)

    # sending the data with proper message:
    if content_type:
        http_response = f"HTTP/1.1 200 OK\r\n Content-Length: {data_length}\r\n Content-Type: {content_type}\r\n\r\n".encode()
        http_response += data
    else:
        print(f"False http header is received: {content_type}.")
        http_response = f"HTTP/1.1 403 Forbidden\r\n".encode()
        http_response += data

    if get_data_validation_flag:
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
