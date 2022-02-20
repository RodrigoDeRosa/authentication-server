from app.database.daos.auth_dao import AuthDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.errors.invalid_password_error import InvalidPasswordError
from app.utils.authentication.password_utils import PasswordUtils


class AuthService:

    @classmethod
    def create_account(cls, creation_dto: AccountCrudDto):
        cls.__verify_password(creation_dto.password)
        AuthDao.store(creation_dto.to_auth_data())

    @classmethod
    def __verify_password(cls, password: str):
        """ Check that the given password matches security standards. """
        if not PasswordUtils.verify_password(password):
            raise InvalidPasswordError(PasswordUtils.PASSWORD_REQUIREMENTS_READABLE)
