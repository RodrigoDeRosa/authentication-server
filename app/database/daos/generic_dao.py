from typing import TypeVar, List

from flask_sqlalchemy import Model

from app.database.connectors.postgres_connector import QueryFilter
from app.database.database_manager import DatabaseManager
from app.utils.logging.logger import Logger


class GenericDao:

    T = TypeVar('T', bound=Model)

    @classmethod
    def _get(cls, model: T, filters: List[QueryFilter]) -> T:
        return cls.__get_connector().get(
            model=model,
            filters=filters
        )

    @classmethod
    def _save(cls, entity: T):
        cls.__get_connector().save(entity=entity)

    @classmethod
    def _update(cls, model: T, filters: List[QueryFilter], fields_to_update: dict) -> T:
        return cls.__get_connector().update(
            model=model,
            filters=filters,
            fields_to_update=fields_to_update
        )

    @classmethod
    def _delete(cls, entity: T):
        cls.__get_connector().delete(entity=entity)

    @classmethod
    def __get_connector(cls):
        return DatabaseManager.connector

    @classmethod
    def _logger(cls):
        return Logger(cls.__name__)
