from unittest import TestCase, mock

from app.database.daos.account_dao import AccountDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.errors.already_existing_resource_error import AlreadyExistingResourceError
from app.service.account.account_service import AccountService
from app.service.auth.auth_service import AuthService


class AccountServiceTest(TestCase):

    def setUp(self) -> None:
        self.creation_dto = AccountCrudDto(
            username='iron.mike',
            first_name='Mike',
            last_name='Tyson',
            password='uppercut')

    @mock.patch.object(AccountDao, 'store')
    @mock.patch.object(AuthService, 'create_account')
    @mock.patch.object(AccountDao, 'find_by_username', return_value=None)
    def test_create_account(self, find_mock, auth_create_mock, dao_store_mock):
        AccountService.create_account(self.creation_dto)

        find_mock.assert_called_with(self.creation_dto.username)
        auth_create_mock.assert_called_with(self.creation_dto)
        dao_store_mock.assert_called_with(self.creation_dto.to_account())

    @mock.patch.object(AccountDao, 'find_by_username')
    def test_create_account_with_existing_username(self, find_mock):
        find_mock.return_value = self.creation_dto.to_account()
        with self.assertRaises(AlreadyExistingResourceError):
            AccountService.create_account(self.creation_dto)
