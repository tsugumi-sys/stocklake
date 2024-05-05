import os
import tempfile
from typing import List

from sqlalchemy import orm

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqApiSymbolData
from stocklake.nasdaqapi.utils import save_data_to_csv
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models, schemas  # noqa: E402
from stocklake.stores.db.database import LocalSession

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "nasdaqapi")


class NASDAQDataStore(BaseStore):
    def save(
        self,
        store_type: StoreType,
        exchange_name: Exchange,
        data: List[NasdaqApiSymbolData],
    ):
        if StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tmpdir:
                csv_file_path = os.path.join(tmpdir, f"{exchange_name}_data.csv")
                save_data_to_csv(data, csv_file_path)
                repository.save_artifact(csv_file_path)


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
        with self.session() as session, session.begin():
            session.query(models.NasdaqApiData).delete()
