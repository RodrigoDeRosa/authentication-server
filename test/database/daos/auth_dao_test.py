from app.database.daos.auth_dao import AuthDao
from app.model.auth.auth_data import AuthData
from test.integration_test_case import IntegrationTestCase


class AuthDaoTest(IntegrationTestCase):

    def test_store_and_retrieve_auth_data(self):
        auth_data = AuthData('username', 'password')
        auth_data.encrypt()

        AuthDao.store(auth_data)

        stored_data = AuthDao.find('username')
        self.assertEqual('username', stored_data.username)
        self.assertTrue(stored_data.check_password('password'))

    def test_retrieve_non_existent_auth_data(self):
        stored_data = AuthDao.find('username')
        self.assertIsNone(stored_data)
