from http import HTTPStatus

from app.model.errors.application_error import ApplicationError


class InvalidLoginDataError(ApplicationError):

    def __init__(self):
        super().__init__(f'Invalid user or password.', HTTPStatus.BAD_REQUEST)
