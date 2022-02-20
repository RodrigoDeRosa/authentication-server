from http import HTTPStatus

from app.model.errors.application_error import ApplicationError


class AlreadyExistingResourceError(ApplicationError):

    def __init__(self, resource_name: str, field_name: str, field_value: str) -> None:
        super().__init__(
            f'{resource_name} with {field_name}:[{field_value}] already exists.',
            HTTPStatus.CONFLICT)
