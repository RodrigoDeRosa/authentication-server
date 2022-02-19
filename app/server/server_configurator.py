from flask import Flask

from app.server.router import Router
from app.utils.logging.logger import Logger


class ServerConfigurator:

    @classmethod
    def configure(cls, app: Flask):
        Logger.set_up()
        Router.register_routes(app)
