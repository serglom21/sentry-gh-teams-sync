class HTTPResponse():

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def get_status_code(self):
        return self.status_code
    
    def get_message(self):
        return self.message