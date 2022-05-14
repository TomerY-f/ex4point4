class ParameterResourceHandler:
    def __init__(self, url=str):
        self.url = url
        self.parameter_type = url.split('?')[0][1:]
        self.parameter_values = url.split('?')[1].split('&')

    def calculation(self):
        if self.parameter_type == 'calculate-next':
            number = self.parameter_values[0].split('=')[1]
            return True, str(int(number) + 1).encode()
        if self.parameter_type == 'calculate-area':
            height = float(self.parameter_values[0].split('=')[1])
            width = float(self.parameter_values[1].split('=')[1])
            area = str(height * width / 2)
            return True, area.encode()
        else:
            print(f'Unknown parameter type: {self.parameter_type}. 404 will send to browser.')
            return False, b''
