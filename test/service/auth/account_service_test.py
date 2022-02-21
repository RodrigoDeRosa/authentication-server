from unittest import TestCase, mock

from app.database.daos.account_dao import AccountDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.auth.auth_data import AuthData
from app.model.errors.already_existing_resource_error import AlreadyExistingResourceError
from app.service.account.account_service import AccountService
from app.service.auth.auth_service import AuthService
from app.utils.authentication.auth_manager import AuthManager


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

    @mock.patch.object(AccountDao, 'find_by_username')
    @mock.patch.object(AuthManager.login_manager, 'current_user', return_value=AuthData('user', '123'))
    def test_get_logged_account(self, auth_mock, find_mock):
        AccountService.get_logged_account()

        self.assertEqual(1, auth_mock.call_count)
        find_mock.assert_called_with('user')

    @mock.patch.object(AccountDao, 'find_by_username')
    @mock.patch.object(AccountDao, 'update')
    @mock.patch.object(AuthService, 'change_password')
    @mock.patch.object(AuthManager.login_manager, 'current_user', return_value=AuthData('user', '123'))
    def test_update_logged_account(self, auth_mock, change_pwd_mock, update_mock, find_mock):
        find_mock.return_value = self.creation_dto.to_account()

        AccountService.update_logged_account(self.creation_dto)

        self.assertEqual(1, auth_mock.call_count)
        find_mock.assert_called_with('user')
        update_mock.assert_called_with(self.creation_dto.to_account())
        change_pwd_mock.assert_called_with(self.creation_dto)

    @mock.patch.object(AccountDao, 'find_by_username')
    @mock.patch.object(AccountDao, 'update')
    @mock.patch.object(AuthService, 'change_password')
    @mock.patch.object(AuthManager.login_manager, 'current_user', return_value=AuthData('user', '123'))
    def test_update_logged_account_no_password(self, auth_mock, change_pwd_mock, update_mock, find_mock):
        update_dto = AccountCrudDto(username=None, first_name='Mike', last_name='Tyson', password=None)
        find_mock.return_value = update_dto.to_account()

        AccountService.update_logged_account(update_dto)

        self.assertEqual(1, auth_mock.call_count)
        find_mock.assert_called_with('user')
        update_mock.assert_called_with(update_dto.to_account())
        self.assertEqual(0, change_pwd_mock.call_count)

    @mock.patch.object(AccountDao, 'delete')
    @mock.patch.object(AuthService, 'delete')
    @mock.patch.object(AuthManager.login_manager, 'current_user', return_value=AuthData('user', '123'))
    def test_delete_logged_account(self, auth_mock, auth_delete_mock, account_delete_mock):
        AccountService.delete_logged_account()

        self.assertEqual(1, auth_mock.call_count)
        account_delete_mock.assert_called_with('user')
        auth_delete_mock.assert_called_with('user')
