from typing import List, Union, NewType

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.operators import ColumnOperators
from app.utils.logging.logger import Logger

from app.database.connectors.abstract_database_connector import AbstractDatabaseConnector

# Type defined to shorten code. The Union shouldn't be needed, it's just to trick the
# linter which can't realize that `Model.attribute = value` is actually a ColumnOperators
# and not a bool
QueryFilter = NewType('QueryFilter', type(Union[ColumnOperators, bool]))


class PostgresConnector(AbstractDatabaseConnector):

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.session = scoped_session(sessionmaker(bind=db.engine))
        self.logger = Logger(self.__class__.__name__)

    def get(self, model: Model, filters: List[QueryFilter]) -> Model:
        try:
            return self.session().query(model).filter(*filters).first()
        finally:
            self.session().close()

    def save(self, entity: Model):
        try:
            self.session().add(entity)
            self.session().commit()
        except:
            self.logger \
                .warning('Rolling back, there was an error saving the entity of type: ' + entity.__class__.__name__)
            self.session().rollback()
            raise
        finally:
            self.session().close()

    def update(self, model: Model, filters: List[QueryFilter], fields_to_update: dict) -> Model:
        result = self.get(model, filters)
        if result:
            for key, value in fields_to_update.items():
                setattr(result, key, value)
            self.save(result)
        return result

    def delete(self, entity):
        try:
            self.session().delete(entity)
            self.session().commit()
        except:
            self.logger \
                .warning('Rolling back, there was an error deleting the entity of type: ' + entity.__class__.__name__)
            self.session().rollback()
            raise
        finally:
            self.session().close()

    def init_db(self):
        self.db.create_all()

    def drop_db(self):
        self.db.drop_all()
