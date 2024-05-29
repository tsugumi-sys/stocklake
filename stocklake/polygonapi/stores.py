import os
import tempfile
from typing import List

from sqlalchemy import orm

from stocklake.core.base_store import BaseStore
from stocklake.core.constants import DATA_DIR
from stocklake.polygonapi.entities import PolygonFinancialsData
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType
from stocklake.stores.db.database import LocalSession  # noqa: E402
from stocklake.utils.file_utils import save_data_to_csv

SAVE_ARTIFACTS_DIR = os.path.join(DATA_DIR, "nasdaqapi")


class PolygonFinancialsDataStore(BaseStore):
    def __init__(
        self, sqlalchemy_session: orm.sessionmaker[orm.session.Session] = LocalSession
    ):
        self.sqlalchemy_session = sqlalchemy_session

    def save(self, store_type: StoreType, data: List[PolygonFinancialsData]):
        if store_type == StoreType.LOCAL_ARTIFACT:
            repository = LocalArtifactRepository(SAVE_ARTIFACTS_DIR)
            with tempfile.TemporaryDirectory() as tempdir:
                csv_file_path = os.path.join(tempdir, "financials_data.csv")
                save_data_to_csv(data, csv_file_path)
                repository.save_artifact(csv_file_path)
        else:
            raise NotImplementedError
