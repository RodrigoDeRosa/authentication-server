from flask import request

from app.controller.abstract_controller import AbstractController
from app.mapper.auth_request_mapper import AuthRequestMapper
from app.service.auth.auth_service import AuthService
from app.utils.authentication.auth_manager import AuthManager


class LoginController(AbstractController):

    def __do_login(self):
        auth_data = AuthRequestMapper.map_login(request.json)

        bearer_token = AuthService.generate_bearer_token(auth_data)

        response = self.build_response({'auth_token': bearer_token})
        response.set_cookie(AuthManager.AUTH_COOKIE_NAME, bearer_token)
        return response

    _post_method = __do_login
