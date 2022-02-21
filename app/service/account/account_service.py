from app.database.daos.account_dao import AccountDao
from app.model.account.account import Account
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.auth.auth_data import AuthData
from app.model.errors.already_existing_resource_error import AlreadyExistingResourceError
from app.service.auth.auth_service import AuthService
from app.utils.authentication.auth_manager import AuthManager


class AccountService:

    __RESOURCE_NAME = 'Account'

    @classmethod
    def create_account(cls, creation_dto: AccountCrudDto):
        if AccountDao.find_by_username(creation_dto.username):
            raise AlreadyExistingResourceError(cls.__RESOURCE_NAME, 'username', creation_dto.username)

        AuthService.create_account(creation_dto)
        AccountDao.store(creation_dto.to_account())

    @classmethod
    def get_logged_account(cls) -> Account:
        auth_data: AuthData = AuthManager.login_manager.current_user()
        return AccountDao.find_by_username(auth_data.username)

    @classmethod
    def update_logged_account(cls, update_dto: AccountCrudDto):
        account = cls.get_logged_account()
        # It would be better to have a separate endpoint for password updating
        # since the new password could be invalid and that should result in a fail
        # to update; for simplicity, I've left this here in this specific order.
        if update_dto.password:
            AuthService.change_password(update_dto)
        AccountDao.update(account)

    @classmethod
    def delete_logged_account(cls):
        username = AuthManager.login_manager.current_user().username
        AccountDao.delete(username)
        AuthService.delete(username)
