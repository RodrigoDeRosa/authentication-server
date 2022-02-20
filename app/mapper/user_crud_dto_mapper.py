from app.model.account.account_crud_dto import AccountCrudDto
from app.utils.mapping.mapping_utils import MappingUtils


class AccountCrudDtoMapper:

    @classmethod
    def map_creation(cls, request_body: dict) -> AccountCrudDto:
        for field in AccountCrudDto.compulsory_fields():
            MappingUtils.check_field_existence(field, request_body)
        return cls.__build_account(request_body)

    @classmethod
    def __build_account(cls, request_body: dict) -> AccountCrudDto:
        return AccountCrudDto(
            username=request_body.get('username'),
            password=request_body.get('password'),
            first_name=request_body.get('first_name'),
            last_name=request_body.get('last_name'))
