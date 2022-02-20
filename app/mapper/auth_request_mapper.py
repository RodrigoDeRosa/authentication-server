from app.model.auth.auth_data import AuthData
from app.utils.mapping.mapping_utils import MappingUtils


class AuthRequestMapper:

    @classmethod
    def map_login(cls, request_body: dict) -> AuthData:
        # Check all compulsory fields are present
        for field in AuthData.compulsory_fields():
            MappingUtils.check_field_existence(field, request_body)
        return AuthData(request_body['username'], request_body['password'])
