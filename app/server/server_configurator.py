from flask import Flask

from app.database.database_manager import DatabaseManager
from app.server.router import Router
from app.utils.configuration.config_holder import ConfigHolder
from app.utils.logging.logger import Logger


class ServerConfigurator:

    @classmethod
    def configure(cls, app: Flask):
        # Needed for signing cookies
        app.secret_key = ConfigHolder.config().get('app.secret')

        Logger.set_up()
        Router.register_routes(app)
        DatabaseManager.set_up(app)

        Logger(cls.__name__).info('Server configuration finished.')
