from app.controller.account.account_management_controller import AccountManagementController
from app.controller.auth.login_controller import LoginController


class AuthRouter:

    @staticmethod
    def routes():
        return {
            LoginController: ['/login'],
            AccountManagementController: ['/accounts/manage']
        }
