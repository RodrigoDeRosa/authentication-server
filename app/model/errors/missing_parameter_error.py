from http import HTTPStatus

from app.model.errors.application_error import ApplicationError


class MissingParameterError(ApplicationError):

    def __init__(self, field_name: str) -> None:
        super(MissingParameterError, self).__init__(f'Missing compulsory field "{field_name}".', HTTPStatus.BAD_REQUEST)
