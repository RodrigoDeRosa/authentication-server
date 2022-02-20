from http import HTTPStatus

from flask import request

from app.controller.abstract_controller import AbstractController
from app.mapper.user_crud_dto_mapper import AccountCrudDtoMapper
from app.service.account.account_service import AccountService


class AccountManagementController(AbstractController):

    def __create_account(self):
        creation_dto = AccountCrudDtoMapper.map_creation(request.json)
        AccountService.create_account(creation_dto)
        return self.build_response(status=HTTPStatus.CREATED)

    def __get_account_data(self):
        pass

    def __update_account_data(self):
        pass

    _post_method = __create_account
    _get_method = __get_account_data
    _put_method = __update_account_data
