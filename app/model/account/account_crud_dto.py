from dataclasses import dataclass

from app.model.account.account import Account
from app.model.auth.auth_data import AuthData


@dataclass
class AccountCrudDto:
    username: str
    first_name: str
    last_name: str
    password: str

    def to_account(self) -> Account:
        return Account(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name)

    def to_auth_data(self) -> AuthData:
        return AuthData(
            username=self.username,
            password=self.password)

    @classmethod
    def compulsory_fields(cls):
        return dict(cls.__annotations__)
