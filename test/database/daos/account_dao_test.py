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

    def test_update_account(self):
        AccountDao.store(Account('rodriderosa', 'Rodrigo', 'De Rosa'))

        update_dto = Account(username='rodriderosa', first_name='Lionel', last_name=None)
        AccountDao.update(update_dto)

        stored_data = AccountDao.find_by_username('rodriderosa')
        self.assertEqual('Lionel', stored_data.first_name)
        self.assertEqual('De Rosa', stored_data.last_name)

    def test_update_account_all_fields(self):
        AccountDao.store(Account('rodriderosa', 'Rodrigo', 'De Rosa'))

        update_dto = Account(username='rodriderosa', first_name='Lionel', last_name='Messi')
        AccountDao.update(update_dto)

        stored_data = AccountDao.find_by_username('rodriderosa')
        self.assertEqual('Lionel', stored_data.first_name)
        self.assertEqual('Messi', stored_data.last_name)

    def test_delete_account(self):
        AccountDao.store(Account('rodriderosa', 'Rodrigo', 'De Rosa'))

        AccountDao.delete('rodriderosa')

        stored_data = AccountDao.find_by_username('rodriderosa')
        self.assertIsNone(stored_data)
