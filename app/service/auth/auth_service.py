from app.database.daos.auth_dao import AuthDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.auth.auth_data import AuthData
from app.model.errors.invalid_login_data_error import InvalidLoginDataError
from app.model.errors.invalid_password_error import InvalidPasswordError
from app.utils.authentication.auth_manager import AuthManager
from app.utils.authentication.password_utils import PasswordUtils


class AuthService:

    @classmethod
    def create_account(cls, creation_dto: AccountCrudDto):
        auth_data = cls.__get_encrypted_data_if_valid(creation_dto)
        AuthDao.store(auth_data)

    @classmethod
    def change_password(cls, update_dto: AccountCrudDto):
        auth_data = cls.__get_encrypted_data_if_valid(update_dto)
        AuthDao.change_password(auth_data)

    @classmethod
    def delete(cls, username: str):
        AuthDao.delete(username)

    @classmethod
    def generate_bearer_token(cls, auth_data: AuthData):
        cls.__verify_auth_data(auth_data)
        return AuthManager.generate_token(auth_data.username)

    @classmethod
    def retrieve_auth_data(cls, username: str) -> AuthData:
        return AuthDao.find(username)

    @classmethod
    def __get_encrypted_data_if_valid(cls, dto: AccountCrudDto) -> AuthData:
        cls.__verify_password(dto.password)
        auth_data = dto.to_auth_data()
        auth_data.encrypt()
        return auth_data

    @classmethod
    def __verify_auth_data(cls, auth_data: AuthData):
        stored_data = AuthDao.find(auth_data.username)

        if not stored_data:
            raise InvalidLoginDataError()
        if not stored_data.check_password(auth_data.password):
            raise InvalidLoginDataError()

    @classmethod
    def __verify_password(cls, password: str):
        if not PasswordUtils.verify_password(password):
            raise InvalidPasswordError(PasswordUtils.PASSWORD_REQUIREMENTS_READABLE)
