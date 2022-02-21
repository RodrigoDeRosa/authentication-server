from http import HTTPStatus
from json import dumps

from related import to_dict

from app.model.account.account_crud_dto import AccountCrudDto
from test.integration_test_case import IntegrationTestCase


class AppIntegrationTest(IntegrationTestCase):

    def setUp(self):
        super(AppIntegrationTest, self).setUp()
        self.account = {
            'username': 'integration',
            'first_name': 'Testy',
            'last_name': 'Integral',
            'password': 'integrationT3st'
        }

    def test_full_user_flow(self):
        """
        It's not great to have everything in one place, but this is a PoC to show
        what we could do with this integration testing suite.
        """
        post_response = self.post_account(self.account)
        self.assertEqual(HTTPStatus.CREATED, post_response.status_code)

        log_in_response = self.log_in()
        self.assertEqual(HTTPStatus.OK, log_in_response.status_code)

        get_account_response = self.get_account()
        self.assertEqual(HTTPStatus.OK, get_account_response.status_code)
        account_body = get_account_response.json
        self.assertIsNotNone(account_body)
        self.assertEqual('Testy', account_body['first_name'])
        self.assertEqual('Integral', account_body['last_name'])
        self.assertEqual('integration', account_body['username'])

        update_account_response = self.update_account({'first_name': 'Jack'})
        self.assertEqual(HTTPStatus.NO_CONTENT, update_account_response.status_code)

        get_updated_account_response = self.get_account()
        self.assertEqual('Jack', get_updated_account_response.json['first_name'])

        delete_account_response = self.delete_account()
        self.assertEqual(HTTPStatus.NO_CONTENT, delete_account_response.status_code)

        get_deleted_account_response = self.get_account()
        self.assertEqual(HTTPStatus.UNAUTHORIZED, get_deleted_account_response.status_code)

    def log_in(self):
        login_response = self.do_login(self.account['username'], self.account['password'])
        self.auth_token = login_response.json['auth_token']
        return login_response

    def do_login(self, username: str, password: str):
        with self.app.test_client() as client:
            response = client.post(
                '/login',
                data=dumps({'username': username, 'password': password}),
                content_type='application/json'
            )
        return response

    def get_account(self):
        with self.app.test_client() as client:
            return client.get(
                f'/accounts/manage',
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )

    def post_account(self, request: dict):
        with self.app.test_client() as client:
            return client.post(
                f'/accounts/manage',
                data=dumps(request),
                content_type='application/json',
            )

    def delete_account(self):
        with self.app.test_client() as client:
            return client.delete(
                f'/accounts/manage',
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )

    def update_account(self, request: dict):
        with self.app.test_client() as client:
            return client.put(
                f'/accounts/manage',
                data=dumps(request),
                content_type='application/json',
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
