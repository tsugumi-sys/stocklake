import os
import tempfile
from typing import List, Optional

from sqlalchemy import orm

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqApiSymbolData
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models, schemas
from stocklake.stores.db.database import local_session
from stocklake.utils.file_utils import save_data_to_csv

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "nasdaqapi")


class NASDAQDataStore(BaseStore):
    def __init__(
        self, sqlalchemy_session: Optional[orm.sessionmaker[orm.session.Session]] = None
    ):
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.sqlalchemy_session = sqlalchemy_session

    def save(
        self,
        store_type: StoreType,
        exchange: Exchange,
        data: List[NasdaqApiSymbolData],
    ):
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tmpdir:
                csv_file_path = os.path.join(tmpdir, f"{exchange}_data.csv")
                save_data_to_csv(data, csv_file_path)
                repository.save_artifact(csv_file_path)
        elif store_type == StoreType.POSTGRESQL:
            if self.sqlalchemy_session is None:
                raise StockLoaderException("`sqlalchemy_session` is None.")
            sqlstore = NasdaqApiSQLAlchemyStore(exchange, self.sqlalchemy_session)
            sqlstore.delete()
            sqlstore.create([schemas.NasdaqStockCreate(**d) for d in data])
        else:
            raise NotImplementedError


class NasdaqApiSQLAlchemyStore(SQLAlchemyStore):
    def __init__(
        self, exchange: Exchange, session: orm.sessionmaker[orm.session.Session]
    ):
        self.exchange = exchange
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
        with self.session() as session, session.begin():
            session.query(models.NasdaqApiData).filter(
                models.NasdaqApiData.exchange == self.exchange
            ).delete()
