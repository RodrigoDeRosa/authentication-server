from related import to_dict

from app.controller.abstract_controller import AbstractController
from app.database.daos.auth_dao import AuthDao
from app.model.auth.auth_data import AuthData


class LoginController(AbstractController):

    def __do_login(self):
        self._get_logger().info("Received login request")

        try:
            AuthDao.store(AuthData('rodricra', '1234'))
        except:
            self._get_logger().warning('rodricra already exists!')

        return self.build_response(to_dict(AuthDao.find('rodricra')))

    _post_method = __do_login
