import os
import tempfile
from typing import List, Optional

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.polygonapi import BASE_SAVE_ARTIFACTS_DIR
from stocklake.polygonapi.aggregates_bars import entities
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.stores.db import models
from stocklake.stores.db.database import (
    DATABASE_SESSION_TYPE,
    local_session,
    safe_database_url_from_sessionmaker,
)
from stocklake.utils.file_utils import save_data_to_csv

SAVE_ARTIFACTS_DIR = os.path.join(BASE_SAVE_ARTIFACTS_DIR, "aggregates_bars")


class PolygonAggregatesBarsDataStore(BaseStore):
    def __init__(self, sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None):
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.sqlalchemy_session = sqlalchemy_session

    def save(
        self,
        store_type: StoreType,
        data: List[entities.PreprocessedPolygonAggregatesBarsData],
        artifact_format: ArtifactFormat | None = None,
    ) -> str:
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tempdir:
                if artifact_format == ArtifactFormat.CSV or artifact_format is None:
                    csv_file_path = os.path.join(tempdir, "aggregates_bars.csv")
                    save_data_to_csv([d.model_dump() for d in data], csv_file_path)
                    repository.save_artifact(csv_file_path)
                else:
                    raise NotImplementedError()
            return repository.list_artifacts()[0].path
        elif store_type == StoreType.POSTGRESQL:
            sqlstore = PolygonAggregatesBarsDataSQLAlchemyStore(self.sqlalchemy_session)
            sqlstore.delete(list(set([d.ticker for d in data])))
            sqlstore.create(
                [
                    entities.PolygonAggregatesBarsDataCreate(**d.model_dump())
                    for d in data
                ]
            )
            return os.path.join(
                safe_database_url_from_sessionmaker(self.sqlalchemy_session),
                models.PolygonAggregatesBarsData.__tablename__,
            )
        else:
            raise NotImplementedError()


class PolygonAggregatesBarsDataSQLAlchemyStore(SQLAlchemyStore):
    def __init__(self, session: DATABASE_SESSION_TYPE):
        self.session = session

    def create(self, data: List[entities.PolygonAggregatesBarsDataCreate]):
        with self.session() as session, session.begin():
            session.add_all(
                [models.PolygonAggregatesBarsData(**d.model_dump()) for d in data]
            )

    def read(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self, tickers: List[str] | None = None):
        with self.session() as session, session.begin():
            if tickers:
                session.query(models.PolygonAggregatesBarsData).filter(
                    models.PolygonAggregatesBarsData.ticker.in_(tickers)
                ).delete()
            else:
                session.query(models.PolygonAggregatesBarsData).delete()
