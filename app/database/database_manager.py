import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.database.connectors.abstract_database_connector import AbstractDatabaseConnector
from app.database.connectors.postgres_connector import PostgresConnector
from app.utils.configuration.config_holder import ConfigHolder
from app.utils.logging.logger import Logger


class DatabaseManager:

    DB: SQLAlchemy = SQLAlchemy()
    connector: AbstractDatabaseConnector = None

    __logger = Logger('DatabaseManager')

    @classmethod
    def set_up(cls, app: Flask):
        cls.__logger.info('Configuring database connection...')

        app.config['SQLALCHEMY_DATABASE_URI'] = cls.build_url()
        # Silence a deprecation warning
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.app_context().push()

        cls.build(app)

    @classmethod
    def build(cls, app: Flask):
        cls.DB.init_app(app)
        # Inject Postgres connector
        cls.connector = PostgresConnector(cls.DB)
        cls.connector.init_db()

    @classmethod
    def build_url(cls):
        # This tiny part is a hack for testing. Test code shouldn't be intertwined
        # with production code but it makes our lives way easier for the scope of this app
        full_url = cls.get_env_variable('DATABASE_FULL_URL')
        if full_url: return full_url

        url = ConfigHolder.config().get('database.url')
        database = ConfigHolder.config().get('database.name')
        user = ConfigHolder.config().get('database.user_name', None)
        password = ConfigHolder.config().get('database.password', None)
        auth_string = None if not password or not user else f'{user}:{password}@'

        return f'postgresql+psycopg2://{"" if not auth_string else auth_string}{url}/{database}'

    @staticmethod
    def get_env_variable(name, raise_exception: bool = False):
        try:
            return os.environ[name]
        except KeyError:
            if raise_exception:
                raise RuntimeError(f'Missing compulsory environment variable {name}')