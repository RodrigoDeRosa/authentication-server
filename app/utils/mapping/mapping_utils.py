from app.model.errors.missing_parameter_error import MissingParameterError


class MappingUtils:

    @classmethod
    def check_field_existence(cls, field: str, request_body: dict):
        if field not in request_body:
            raise MissingParameterError(field)
