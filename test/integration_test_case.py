import os

from flask import Flask
from flask_testing import TestCase

from app.database.database_manager import DatabaseManager
from app.server.server_configurator import ServerConfigurator


class IntegrationTestCase(TestCase):

    def create_app(self):
        os.environ['APP_SECRET'] = 'fakeSecret'
        # Having an in memory database makes testing easier. Given that
        # PostgreSQL doesn't allow to have an in memory DB, we use SQLite
        # for simplicity.
        # `alchemy-mock` seems to be another good option: https://pypi.org/project/alchemy-mock/
        os.environ['DATABASE_FULL_URL'] = 'sqlite:///:memory:'

        test_app = Flask(__name__)
        test_app.config['TESTING'] = True

        ServerConfigurator.configure(test_app)
        return test_app

    def setUp(self):
        DatabaseManager.DB.create_all()

    def tearDown(self):
        DatabaseManager.DB.session.remove()
        DatabaseManager.DB.drop_all()
