from app.controllers.auth.account_management_controller import AccountManagementController
from app.controllers.auth.login_controller import LoginController
from app.controllers.auth.password_management_controller import PasswordManagementController


class AuthRouter:

    @staticmethod
    def routes():
        return {
            LoginController: ['/login'],
            AccountManagementController: ['/accounts/manage'],
            PasswordManagementController: ['/accounts/password']
        }
