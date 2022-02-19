from typing import Optional

from app.database.daos.generic_dao import GenericDAO
from app.database.dtos.auth_dto import AuthDTO
from app.model.auth.auth_data import AuthData


class AuthDAO(GenericDAO):

    @classmethod
    def find(cls, username: str) -> Optional[AuthData]:
        auth_dto = cls._get(AuthDTO, [AuthDTO.username == username])
        if auth_dto:
            return cls.__to_model(auth_dto)

    @classmethod
    def store(cls, auth_data: AuthData):
        cls._save(cls.__to_dto(auth_data))

    @classmethod
    def __to_dto(cls, auth_data: AuthData) -> AuthDTO:
        return AuthDTO(auth_data.username, auth_data.password)

    @classmethod
    def __to_model(cls, auth_dto: AuthDTO) -> AuthData:
        return AuthData(
            username=auth_dto.username,
            password=auth_dto.password)
