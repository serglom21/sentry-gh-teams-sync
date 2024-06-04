class MissingParametersException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def get_message(self):
        return self.message