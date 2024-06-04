class GithubResponse():

    def __init__(self, status_code, message, data = None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def get_status_code(self):
        return self.status_code
    
    def get_message(self):
        return self.message
    
    def get_data(self):
        return self.data