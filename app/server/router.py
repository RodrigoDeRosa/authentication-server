from flask import Flask
from flask_restful import Api

from app.server.routing.auth_router import AuthRouter
from app.utils.logging.logger import Logger


class Router:

    ROUTERS = [
        AuthRouter
    ]

    @classmethod
    def register_routes(cls, app: Flask):
        Logger(cls.__name__).info('Configuring application routing...')

        api = Api(app)
        for router in cls.ROUTERS:
            for controller, endpoints in router.routes().items():
                api.add_resource(controller, *endpoints)
