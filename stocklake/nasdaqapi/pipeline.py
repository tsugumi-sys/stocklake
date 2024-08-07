import json
import logging
from typing import Optional

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.core.base_store import BaseStore
from stocklake.core.stdout import PipelineStdOut
from stocklake.exceptions import StockLakeException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import (
    NASDAQSymbolsDataLoader,
)
from stocklake.nasdaqapi.preprocessor import (
    NASDAQSymbolsPreprocessor,
)
from stocklake.nasdaqapi.stores import NASDAQDataStore
from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.stores.db.database import DATABASE_SESSION_TYPE, local_session
from stocklake.utils.validation import validate_artifact_format, validate_store_type

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(BasePipeline):
    def __init__(
        self,
        skip_download: bool = False,
        exchange: Optional[Exchange] = None,
        store_type: StoreType | None = None,
        artifact_format: ArtifactFormat | None = None,
        sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None,
    ):
        if exchange is not None and exchange not in Exchange.exchanges():
            raise StockLakeException(
                f"Specified exchange is invalid, but got {exchange}. The valid exchanges are {Exchange.exchanges()}"
            )
        self.exchange = exchange
        self.skip_download = skip_download

        if store_type is not None:
            validate_store_type(store_type)
        self.store_type = store_type
        if artifact_format is not None:
            validate_artifact_format(artifact_format)
        self.artifact_format = artifact_format
        self.preprocessor = NASDAQSymbolsPreprocessor()
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.store = NASDAQDataStore(sqlalchemy_session)
        self.stdout = PipelineStdOut(
            enable_stdout=store_type is not None
        )  # MEMO: pipe doesn't work if other output comes into the stdout.

    def run(self):
        if self.exchange is None:
            self.run_all()
            return

        self._run(
            self.exchange,
            NASDAQSymbolsDataLoader(exchange_name=self.exchange),
            self.preprocessor,
            self.store,
        )

    def run_all(self):
        for exchange in Exchange.exchanges():
            self._run(
                exchange,
                NASDAQSymbolsDataLoader(exchange_name=exchange),
                self.preprocessor,
                self.store,
            )

    def _run(
        self,
        exchange: Exchange,
        data_loader: BaseDataLoader,
        preprocessor: BasePreprocessor,
        store: BaseStore,
    ):
        self.stdout.starting(f"NASDAQ API of {exchange.upper()}")
        if not self.skip_download:
            self.stdout.downloading()
            raw_data = data_loader.download()
        else:
            self.stdout.skip_downloading()
            # TODO: fetch from cached file
            return
        data = preprocessor.process(exchange, raw_data)
        if self.store_type:
            stored_location = store.save(
                self.store_type, exchange, data, self.artifact_format
            )
            self.stdout.completed(stored_location)
        else:
            # MEMO: output a serialized json to the stdout for pipe.
            print(json.dumps([d.model_dump() for d in data]), flush=True)
