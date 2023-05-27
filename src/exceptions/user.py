class UserException(Exception):
    """Ошибки пользователей"""
    def __init__(self, status_code: int = 400, message: str = "Some problem with user data"):
        self.status_code = status_code
        self.message = message

class UserCreateException(UserException):
    pass


class UserDeleteException(UserException):
    pass