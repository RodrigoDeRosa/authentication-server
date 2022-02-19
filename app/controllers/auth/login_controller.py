from related import to_dict

from app.controllers.abstract_controller import AbstractController
from app.database.daos.auth_dao import AuthDAO
from app.model.auth.auth_data import AuthData


class LoginController(AbstractController):

    def __do_login(self):
        self._get_logger().info("Received login request")

        try:
            AuthDAO.store(AuthData('rodricra', '1234'))
        except:
            self._get_logger().warning('rodricra already exists!')

        return self.build_response(to_dict(AuthDAO.find('rodricra')))

    _post_method = __do_login
