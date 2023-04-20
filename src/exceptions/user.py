class UserException(Exception):
    def __init__(self, status_code: int = 400, message: str = "Some problem with user data"):
        self.status_code = status_code
        self.message = message

class UserCreateException(UserException):
    pass
