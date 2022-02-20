from app.database.daos.account_dao import AccountDao
from app.model.account.account import Account
from test.integration_test_case import IntegrationTestCase


class AccountDaoTest(IntegrationTestCase):

    def test_store_and_retrieve_auth_data(self):
        AccountDao.store(Account('rodriderosa', 'Rodrigo', 'De Rosa'))
        stored_data = AccountDao.find_by_username('rodriderosa')
        self.assertEqual('rodriderosa', stored_data.username)
        self.assertEqual('Rodrigo', stored_data.first_name)
        self.assertEqual('De Rosa', stored_data.last_name)

    def test_retrieve_non_existent_account(self):
        stored_data = AccountDao.find_by_username('rodriderosa')
        self.assertIsNone(stored_data)