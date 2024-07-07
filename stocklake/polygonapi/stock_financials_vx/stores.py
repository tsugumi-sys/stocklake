import os
import tempfile
from typing import List, Optional

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.polygonapi.stock_financials_vx import entities
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models
from stocklake.stores.db.database import (
    DATABASE_SESSION_TYPE,
    local_session,
    safe_database_url_from_sessionmaker,
)
from stocklake.utils.file_utils import save_data_to_csv

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "polygonapi")


class PolygonFinancialsDataStore(BaseStore):
    def __init__(self, sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None):
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.sqlalchemy_session = sqlalchemy_session

    def save(
        self,
        store_type: StoreType,
        data: List[entities.PreprocessedPolygonFinancialsData],
    ) -> str:
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tempdir:
                csv_file_path = os.path.join(tempdir, "financials_data.csv")
                save_data_to_csv([d.model_dump() for d in data], csv_file_path)
                repository.save_artifact(csv_file_path)
            return repository.list_artifacts()[0].path
        elif store_type == StoreType.POSTGRESQL:
            sqlstore = PolygonFinancialsDataSQLAlchemyStore(self.sqlalchemy_session)
            sqlstore.delete()
            sqlstore.create(
                [entities.PolygonFinancialsDataCreate(**d.model_dump()) for d in data]
            )
            return os.path.join(
                safe_database_url_from_sessionmaker(self.sqlalchemy_session),
                models.PolygonFinancialsData.__tablename__,
            )
        else:
            raise NotImplementedError()


class PolygonFinancialsDataSQLAlchemyStore(SQLAlchemyStore):
    def __init__(self, session: DATABASE_SESSION_TYPE):
        self.session = session

    def create(self, data: List[entities.PolygonFinancialsDataCreate]):
        with self.session() as session, session.begin():
            session.add_all(
                [models.PolygonFinancialsData(**d.model_dump()) for d in data]
            )

    def read(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self):
        with self.session() as session, session.begin():
            session.query(models.PolygonFinancialsData).delete()
