import logging
from typing import Optional

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import (
    AMEXSymbolsDataLoader,
    NASDAQSymbolsDataLoader,
    NYSESymbolsDataLoader,
)
from stocklake.nasdaqapi.preprocessor import (
    AMEXSymbolsPreprocessor,
    NASDAQSymbolsPreprocessor,
    NYSESymbolsPreprocessor,
)
from stocklake.nasdaqapi.store import NASDAQDataStore
from stocklake.stores.constants import StoreType

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(BasePipeline):
    def __init__(
        self,
        skip_download: bool = False,
        exchange: Optional[Exchange] = None,
        store_type: StoreType = StoreType.LOCAL_ARTIFACT,
    ):
        self.exchange = exchange
        self.skip_download = skip_download

        if store_type not in StoreType.types():
            raise StockLoaderException(
                f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
            )
        self.store_type = store_type
        self.stdout = PrettyStdoutPrint()

    def run(self):
        logger.info("{} NASDAQ pipeline starts {}".format("=" * 30, "=" * 30))

        if self.exchange == Exchange.NASDAQ or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NASDAQ} symbols with nasdapapi")
            data_loader = NASDAQSymbolsDataLoader()
            preprocessor = NASDAQSymbolsPreprocessor()
            self._run(Exchange.NASDAQ, data_loader, preprocessor)

        if self.exchange == Exchange.NYSE or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NYSE} symbols with nasdapapi")
            data_loader = NYSESymbolsDataLoader()
            preprocessor = NYSESymbolsPreprocessor()
            self._run(Exchange.NYSE, data_loader, preprocessor)

        if self.exchange == Exchange.AMEX or self.exchange is None:
            self.stdout.step_start(f"{Exchange.AMEX} symbols with nasdapapi")
            data_loader = AMEXSymbolsDataLoader()
            preprocessor = AMEXSymbolsPreprocessor()
            self._run(Exchange.AMEX, data_loader, preprocessor)

    def _run(
        self,
        exchange: Exchange,
        data_loader: BaseDataLoader,
        preprocessor: BasePreprocessor,
    ):
        if not self.skip_download:
            self.stdout.normal_message("- Downloading ...")
            raw_data = data_loader.download()
        else:
            self.stdout.warning_message("- Skip Downloading")
            # TODO: fetch from cached file
            return
        data = preprocessor.process(raw_data)
        store = NASDAQDataStore()
        store.save(self.store_type, exchange, data)
        self.stdout.success_message("- Completed🐳.")
