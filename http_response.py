from http_conventions import CONTENT_TYPE_HEADER


class HttpResponse:
    def __init__(self, version='HTTP/1.1', response_code=str, content_type=CONTENT_TYPE_HEADER['txt'], data=b''):
        self.version = version
        self.response_code = response_code
        self.content_type = content_type
        self.data = data
        self.content_length = len(data)

    def build_http_response(self):
        http_response = f"{self.version} {self.response_code}\r\n Content-Length: {self.content_length}\r\n Content-Type: {self.content_type}\r\n\r\n".encode()
        http_response += self.data
        return http_response
