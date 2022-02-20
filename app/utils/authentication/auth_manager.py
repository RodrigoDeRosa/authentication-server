from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.utils.configuration.config_holder import ConfigHolder
from app.utils.logging.logger import Logger
import time


class AuthManager:

    login_manager = HTTPTokenAuth('Bearer')
    AUTH_COOKIE_NAME = ConfigHolder.config().get('auth.cookie_name')

    __token_serializer: Serializer = None
    __TOKEN_DURATION_SECS = ConfigHolder.config().get('auth.token.duration')

    @classmethod
    def set_up(cls, app: Flask):
        Logger(cls.__name__).info('Configuring authentication manager...')
        cls.login_manager.verify_token(cls.__verify_token)
        cls.__token_serializer = Serializer(app.secret_key, expires_in=cls.__TOKEN_DURATION_SECS)

    @classmethod
    def generate_token(cls, username: str) -> str:
        token_data = {
            'username': username,
            'expiration': int(round((time.time() + cls.__TOKEN_DURATION_SECS) * 1000))
        }
        return cls.__token_serializer.dumps(token_data).decode('utf-8')

    @classmethod
    def __verify_token(cls, token: str):
        # This is done here to avoid circular import errors
        from app.service.auth.auth_service import AuthService
        try:
            cookie_auth = request.cookies.get(cls.AUTH_COOKIE_NAME)
            received_token = cookie_auth if cookie_auth else token

            token_data = cls.__token_serializer.loads(received_token)
            return AuthService.retrieve_auth_data(token_data['username'])
        except:
            return False
