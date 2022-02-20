from typing import Optional

from app.database.daos.generic_dao import GenericDao
from app.database.dtos.account_dto import AccountDto
from app.model.account.account import Account


class AccountDao(GenericDao):

    @classmethod
    def find_by_username(cls, username: str) -> Optional[Account]:
        account = cls._get(AccountDto, [AccountDto.username == username])
        return cls.__to_model(account)

    @classmethod
    def store(cls, account: Account):
        cls._save(cls.__to_dto(account))

    @staticmethod
    def __to_dto(account: Account) -> AccountDto:
        return AccountDto(
            username=account.username,
            first_name=account.first_name,
            last_name=account.last_name)

    @staticmethod
    def __to_model(account_dto: AccountDto) -> Optional[Account]:
        if not account_dto: return None
        return Account(
            username=account_dto.username,
            first_name=account_dto.first_name,
            last_name=account_dto.last_name)
