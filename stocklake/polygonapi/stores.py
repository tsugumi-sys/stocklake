import os
import tempfile
from typing import List, Optional

from sqlalchemy import orm

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models, schemas
from stocklake.stores.db.database import local_session
from stocklake.utils.file_utils import save_data_to_csv

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "polygonapi")


class PolygonFinancialsDataStore(BaseStore):
    def __init__(
        self, sqlalchemy_session: Optional[orm.sessionmaker[orm.session.Session]] = None
    ):
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.sqlalchemy_session = sqlalchemy_session

    def save(
        self,
        store_type: StoreType,
        data: List[schemas.PreprocessedPolygonFinancialsData],
    ):
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tempdir:
                csv_file_path = os.path.join(tempdir, "financials_data.csv")
                save_data_to_csv([d.dict() for d in data], csv_file_path)
                repository.save_artifact(csv_file_path)
        elif store_type == StoreType.POSTGRESQL:
            sqlstore = PolygonFinancialsDataSQLAlchemyStore(self.sqlalchemy_session)
            sqlstore.delete()
            sqlstore.create(
                [schemas.PolygonFinancialsDataCreate(**d.dict()) for d in data]
            )
        else:
            raise NotImplementedError


class PolygonFinancialsDataSQLAlchemyStore(SQLAlchemyStore):
    def __init__(self, session: orm.sessionmaker[orm.session.Session]):
        self.session = session

    def create(self, data: List[schemas.PolygonFinancialsDataCreate]):
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
