from app.controllers.abstract_controller import AbstractController
from app.utils.logging.logger import Logger


class LoginController(AbstractController):

    __logger = Logger('LoginController')

    def __do_login(self):
        self.__logger.info("Received login request")

    _post_method = __do_login
