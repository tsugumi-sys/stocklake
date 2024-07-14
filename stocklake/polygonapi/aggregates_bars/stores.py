import os
import tempfile
from typing import List, Optional

from stocklake.core.base_store import BaseStore
from stocklake.polygonapi import BASE_SAVE_ARTIFACTS_DIR
from stocklake.polygonapi.aggregates_bars import entities
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db.database import (
    DATABASE_SESSION_TYPE,
    local_session,
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
    ) -> str:
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tempdir:
                csv_file_path = os.path.join(tempdir, "aggregates_bars.csv")
                save_data_to_csv([d.model_dump() for d in data], csv_file_path)
                repository.save_artifact(csv_file_path)
            return repository.list_artifacts()[0].path
        # elif store_type == StoreType.POSTGRESQL:
        else:
            raise NotImplementedError()
