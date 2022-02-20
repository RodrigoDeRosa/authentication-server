from http import HTTPStatus

from app.model.errors.application_error import ApplicationError


class InvalidPasswordError(ApplicationError):

    def __init__(self, requirements: str):
        super().__init__(
            f'Password does not meet security requirements. {requirements}',
            HTTPStatus.BAD_REQUEST)
