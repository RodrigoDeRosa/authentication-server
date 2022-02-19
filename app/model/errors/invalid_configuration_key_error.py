from http import HTTPStatus

from app.model.errors.application_error import ApplicationError


class InvalidConfigurationKeyError(ApplicationError):

    def __init__(self, key: str) -> None:
        super().__init__(
            message=f'Failed to read value with key "{key}".',
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
