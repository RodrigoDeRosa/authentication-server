from app.database.daos.account_dao import AccountDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.errors.already_existing_resource_error import AlreadyExistingResourceError
from app.service.auth.auth_service import AuthService


class AccountService:

    __RESOURCE_NAME = 'Account'

    @classmethod
    def create_account(cls, creation_dto: AccountCrudDto):
        if AccountDao.find_by_username(creation_dto.username):
            raise AlreadyExistingResourceError(cls.__RESOURCE_NAME, 'username', creation_dto.username)

        AuthService.create_account(creation_dto)
        AccountDao.store(creation_dto.to_account())
