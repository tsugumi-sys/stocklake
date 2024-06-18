import logging
from typing import Optional

from sqlalchemy import orm

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.core.base_store import BaseStore
from stocklake.core.stdout import PipelineStdOut
from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import (
    NASDAQSymbolsDataLoader,
)
from stocklake.nasdaqapi.preprocessor import (
    NASDAQSymbolsPreprocessor,
)
from stocklake.nasdaqapi.stores import NASDAQDataStore
from stocklake.stores.constants import StoreType
from stocklake.stores.db.database import local_session

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(BasePipeline):
    def __init__(
        self,
        skip_download: bool = False,
        exchange: Optional[Exchange] = None,
        store_type: StoreType = StoreType.LOCAL_ARTIFACT,
        sqlalchemy_session: Optional[orm.sessionmaker[orm.session.Session]] = None,
    ):
        self.exchange = exchange
        self.skip_download = skip_download

        if store_type not in StoreType.types():
            raise StockLoaderException(
                f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
            )
        self.store_type = store_type
        self.preprocessor = NASDAQSymbolsPreprocessor()
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()
        self.store = NASDAQDataStore(sqlalchemy_session)
        self.stdout = PipelineStdOut()

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
        store.save(self.store_type, exchange, data)
        self.stdout.completed()
