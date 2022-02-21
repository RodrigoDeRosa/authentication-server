from dataclasses import dataclass
from unittest import TestCase, mock

from app.database.daos.auth_dao import AuthDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.errors.invalid_login_data_error import InvalidLoginDataError
from app.model.errors.invalid_password_error import InvalidPasswordError
from app.service.auth.auth_service import AuthService
from app.utils.authentication.auth_manager import AuthManager
from app.utils.authentication.password_utils import PasswordUtils


class AccountServiceTest(TestCase):

    def setUp(self) -> None:
        self.creation_dto = AccountCrudDto(
            username='fran.cuervo',
            first_name='Mario',
            last_name='Bergoglio',
            password='volvemos_a_boedo')

    @mock.patch.object(AuthDao, 'store')
    @mock.patch.object(PasswordUtils, 'verify_password', return_value=True)
    def test_create_account(self, verify_mock, store_mock):
        AuthService.create_account(self.creation_dto)

        verify_mock.assert_called_with(self.creation_dto.password)
        store_mock.assert_called_with(self.AuthDataComparator(self.creation_dto))

    @mock.patch.object(PasswordUtils, 'verify_password', return_value=False)
    def test_create_account_with_invalid_password(self, verify_mock):
        with self.assertRaises(InvalidPasswordError):
            AuthService.create_account(self.creation_dto)

    @mock.patch.object(AuthDao, 'change_password')
    @mock.patch.object(PasswordUtils, 'verify_password', return_value=True)
    def test_change_password(self, verify_mock, change_pwd_mock):
        AuthService.change_password(self.creation_dto)

        verify_mock.assert_called_with(self.creation_dto.password)
        change_pwd_mock.assert_called_with(self.AuthDataComparator(self.creation_dto))

    @mock.patch.object(PasswordUtils, 'verify_password', return_value=False)
    def test_change_password_with_invalid_password(self, verify_mock):
        with self.assertRaises(InvalidPasswordError):
            AuthService.change_password(self.creation_dto)

    @mock.patch.object(AuthManager, 'generate_token', return_value='a-magic-token')
    @mock.patch.object(AuthDao, 'find')
    def test_generate_bearer_token(self, find_mock, token_mock):
        encrypted_data = self.creation_dto.to_auth_data()
        encrypted_data.encrypt()
        find_mock.return_value = encrypted_data

        AuthService.generate_bearer_token(self.creation_dto.to_auth_data())

        find_mock.assert_called_with(self.creation_dto.username)
        token_mock.assert_called_with(self.creation_dto.username)

    @mock.patch.object(AuthDao, 'find', return_value=None)
    def test_generate_bearer_token_invalid_user(self, find_mock):
        with self.assertRaises(InvalidLoginDataError):
            AuthService.generate_bearer_token(self.creation_dto.to_auth_data())

    @mock.patch.object(AuthDao, 'find')
    def test_generate_bearer_token_invalid_password(self, find_mock):
        # Not encrypted password will fail the password check
        find_mock.return_value = self.creation_dto.to_auth_data()
        with self.assertRaises(InvalidLoginDataError):
            AuthService.generate_bearer_token(self.creation_dto.to_auth_data())

    @dataclass
    class AuthDataComparator:
        dto: AccountCrudDto

        def __eq__(self, other):
            return self.dto.username == other.username and other.check_password(self.dto.password)
