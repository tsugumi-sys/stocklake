import json
import logging
from typing import List, Optional

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.core.base_store import BaseStore
from stocklake.core.stdout import PipelineStdOut
from stocklake.polygonapi.aggregates_bars.data_loader import (
    PolygonAggregatesBarsDataLoader,
)
from stocklake.polygonapi.aggregates_bars.preprocessor import (
    PolygonAggregatesBarsPreprocessor,
)
from stocklake.polygonapi.aggregates_bars.stores import PolygonAggregatesBarsDataStore
from stocklake.stores.constants import StoreType
from stocklake.stores.db.database import DATABASE_SESSION_TYPE, local_session
from stocklake.utils.validation import validate_store_type

logger = logging.getLogger(__name__)


class PolygonAggregatesBarsDataPipeline(BasePipeline):
    def __init__(
        self,
        symbols: List[str],
        skip_download: bool = False,
        store_type: StoreType | None = None,
        sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None,
    ):
        self.symbols = symbols
        self.skip_download = skip_download

        if store_type is not None:
            validate_store_type(store_type)
        self.store_type = store_type
        self.data_loader = PolygonAggregatesBarsDataLoader(use_cache=self.skip_download)
        self.preprocessor = PolygonAggregatesBarsPreprocessor()
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.store = PolygonAggregatesBarsDataStore(sqlalchemy_session)
        self.stdout = PipelineStdOut(enable_stdout=store_type is not None)

    def run(self):
        for symbol in self.symbols:
            self._run(symbol, self.data_loader, self.preprocessor, self.store)

    def _run(
        self,
        symbol: str,
        data_loader: BaseDataLoader,
        preprocessor: BasePreprocessor,
        store: BaseStore,
    ):
        self.stdout.starting(f"Aggregates Bars API Polygon of {symbol}")
        if not self.skip_download:
            self.stdout.downloading()
        else:
            self.stdout.skip_downloading()
        raw_data = data_loader.download(self.symbols)
        data = preprocessor.process(raw_data)
        if self.store_type is not None:
            saved_location = store.save(self.store_type, data)
            self.stdout.completed(saved_location)
        else:
            # MEMO: output a serialized json to the stdout for pipe.
            print(json.dumps([d.model_dump() for d in data]), flush=True)