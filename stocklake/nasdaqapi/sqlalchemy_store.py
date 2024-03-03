from typing import List

from sqlalchemy import orm

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.stores.db import models, schemas
from stocklake.stores.db.database import LocalSession


class NasdaqApiSQLAlchemyStore(SQLAlchemyStore):
    def __init__(self, session: orm.sessionmaker[orm.session.Session] = LocalSession):
        self.session = session

    def create(self, data: schemas.NasdaqStockCreate | List[schemas.NasdaqStockCreate]):
        with self.session() as session, session.begin():
            if isinstance(data, list):
                session.add_all([models.NasdaqApiData(**d.model_dump()) for d in data])
            else:
                session.add(models.NasdaqApiData(**data.model_dump()))

    def read(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()
