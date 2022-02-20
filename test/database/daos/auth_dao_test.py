from app.database.daos.auth_dao import AuthDao
from app.model.auth.auth_data import AuthData
from test.integration_test_case import IntegrationTestCase


class AuthDaoTest(IntegrationTestCase):

    def test_store_and_retrieve_auth_data(self):
        AuthDao.store(AuthData('username', 'password'))
        stored_data = AuthDao.find('username')
        self.assertEqual('username', stored_data.username)
        self.assertEqual('password', stored_data.password)

    def test_retrieve_non_existent_auth_data(self):
        stored_data = AuthDao.find('username')
        self.assertIsNone(stored_data)
