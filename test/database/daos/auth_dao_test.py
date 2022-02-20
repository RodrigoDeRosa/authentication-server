from app.database.daos.auth_dao import AuthDAO
from app.model.auth.auth_data import AuthData
from test.integration_test_case import IntegrationTestCase


class AuthDAOTest(IntegrationTestCase):

    def test_store_and_retrieve_auth_data(self):
        AuthDAO.store(AuthData('username', 'password'))
        stored_data = AuthDAO.find('username')
        self.assertEqual('username', stored_data.username)
        self.assertEqual('password', stored_data.password)
