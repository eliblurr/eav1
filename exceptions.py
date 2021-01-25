class NotFoundError(Exception):
    def __init__(self, message:str=None):
        self.message = message

class UnAcceptableError(Exception):
    def __init__(self, message:str=None):
        self.message = message