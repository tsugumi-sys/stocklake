import os
import tempfile
from typing import List, Optional

from stocklake.core.base_sqlalchemy_store import SQLAlchemyStore
from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models
from stocklake.stores.db.database import (
    DATABASE_SESSION_TYPE,
    database_url,
    local_session,
)
from stocklake.utils.file_utils import save_data_to_csv
from stocklake.wiki_sp500 import entities

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "wiki_sp500")


class WikiSP500Store(BaseStore):
    def __init__(self, sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None):
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.sqlalchemy_session = sqlalchemy_session

    def save(
        self, store_type: StoreType, data: List[entities.PreprocessedWikiSp500Data]
    ) -> str:
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tmpdir:
                csv_file_path = os.path.join(tmpdir, "wiki_sp500.csv")
                save_data_to_csv([d.model_dump() for d in data], csv_file_path)
                repository.save_artifact(csv_file_path)
            return repository.list_artifacts()[0].path
        elif store_type == StoreType.POSTGRESQL:
            store = WikiSP500DataSQLAlchemyStore(self.sqlalchemy_session)
            store.delete()
            store.create([entities.WikiSP500DataCreate(**d.model_dump()) for d in data])
            return os.path.join(database_url(), models.WikiSP500Data.__tablename__)
        else:
            raise NotImplementedError()


class WikiSP500DataSQLAlchemyStore(SQLAlchemyStore):
    def __init__(self, session: DATABASE_SESSION_TYPE):
        self.session = session

    def create(self, data: List[entities.WikiSP500DataCreate]):
        with self.session() as session, session.begin():
            session.add_all([models.WikiSP500Data(**d.model_dump()) for d in data])

    def read(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self):
        with self.session() as session, session.begin():
            session.query(models.WikiSP500Data).delete()
