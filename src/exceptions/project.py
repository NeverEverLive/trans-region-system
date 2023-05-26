class ProjectException(Exception):
    def __init__(self, status_code: int = 400, message: str = "Some problem with project data"):
        self.status_code = status_code
        self.message = message

class ProjectCreateException(ProjectException):
    pass


class ProjectDeleteException(ProjectException):
    pass
