from http import HTTPStatus


class ApplicationError(RuntimeError):

    def __init__(self, message: str, status: int = HTTPStatus.INTERNAL_SERVER_ERROR) -> None:
        self.message = message
        self.status = status

    def __str__(self):
        return self.message
