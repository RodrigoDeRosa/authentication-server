import abc


class AbstractDatabaseConnector(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def init_db(self):
        raise NotImplementedError

    @abc.abstractmethod
    def drop_db(self):
        raise NotImplementedError

