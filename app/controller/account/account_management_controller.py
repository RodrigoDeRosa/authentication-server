from http import HTTPStatus

from flask import request

from app.controller.abstract_controller import AbstractController
from app.mapper.account_crud_dto_mapper import AccountCrudDtoMapper
from app.service.account.account_service import AccountService
from app.utils.authentication.auth_manager import AuthManager


class AccountManagementController(AbstractController):

    def __create_account(self):
        creation_dto = AccountCrudDtoMapper.map_creation(request.json)
        AccountService.create_account(creation_dto)
        return self.build_response(status=HTTPStatus.CREATED)

    @AuthManager.login_manager.login_required()
    def __get_account_data(self):
        account = AccountService.get_logged_account()
        return self.build_response(AccountCrudDtoMapper.map_account_data_response(account))

    @AuthManager.login_manager.login_required()
    def __update_account_data(self):
        update_dto = AccountCrudDtoMapper.map_update(request.json)
        AccountService.update_logged_account(update_dto)
        return self.build_response(status=HTTPStatus.NO_CONTENT)

    @AuthManager.login_manager.login_required()
    def __delete_account(self):
        AccountService.delete_logged_account()
        return self.build_response(status=HTTPStatus.NO_CONTENT)

    _post_method = __create_account
    _get_method = __get_account_data
    _put_method = __update_account_data
    _delete_method = __delete_account
