from abc import ABC, abstractmethod

from sqlalchemy import orm


class BaseStore(ABC):
    def __init__(self, sqlalchemy_session: orm.sessionmaker[orm.session.Session]):
        self.sqlalchemy_session = sqlalchemy_session

    @abstractmethod
    def save(self, *args, **kwargs):
        pass
