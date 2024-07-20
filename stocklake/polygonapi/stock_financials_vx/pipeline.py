import json
import logging
from typing import List, Optional

from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.stdout import PipelineStdOut
from stocklake.polygonapi.stock_financials_vx.data_loader import (
    PolygonFinancialsDataLoader,
)
from stocklake.polygonapi.stock_financials_vx.preprocessor import (
    PolygonFinancialsDataPreprocessor,
)
from stocklake.polygonapi.stock_financials_vx.stores import PolygonFinancialsDataStore
from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.stores.db.database import DATABASE_SESSION_TYPE, local_session
from stocklake.utils.validation import validate_artifact_format, validate_store_type

logger = logging.getLogger(__name__)


class PolygonFinancialsDataPipeline(BasePipeline):
    def __init__(
        self,
        symbols: List[str],
        skip_download: bool = False,
        store_type: StoreType | None = None,
        artifact_format: ArtifactFormat | None = None,
        interval_sec: int = 0,
        sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None,
    ):
        self.symbols = symbols
        self.skip_download = skip_download

        if store_type is not None:
            validate_store_type(store_type)
        self.store_type = store_type
        if artifact_format is not None:
            validate_artifact_format(artifact_format)
        self.artifact_format = artifact_format

        self.data_loader = PolygonFinancialsDataLoader(interval_sec)
        self.preprocessor = PolygonFinancialsDataPreprocessor()
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.store = PolygonFinancialsDataStore(sqlalchemy_session)
        self.stdout = PipelineStdOut(
            enable_stdout=store_type is not None
        )  # MEMO: pipe doesn't work if other output comes into the stdout.

    def run(self):
        self.stdout.starting(f"Stock Financials VX API Polygon of {self.symbols}")
        if not self.skip_download:
            self.stdout.downloading()
            raw_data = self.data_loader.download(self.symbols)
        else:
            self.stdout.skip_downloading()
            # TODO: fetch from cached file
            return
        data = self.preprocessor.process(raw_data)
        if self.store_type is not None:
            saved_location = self.store.save(
                self.store_type, data, self.artifact_format
            )
            self.stdout.completed(saved_location)
        else:
            # MEMO: output a serialized json to the stdout for pipe.
            print(json.dumps([d.model_dump() for d in data]), flush=True)
