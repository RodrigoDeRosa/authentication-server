from dataclasses import dataclass
from unittest import TestCase, mock

from app.database.daos.auth_dao import AuthDao
from app.model.account.account_crud_dto import AccountCrudDto
from app.model.errors.invalid_password_error import InvalidPasswordError
from app.service.auth.auth_service import AuthService
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

    @dataclass
    class AuthDataComparator:
        dto: AccountCrudDto

        def __eq__(self, other):
            return self.dto.username == other.username and other.check_password(self.dto.password)
