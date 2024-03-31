import logging
import os
from typing import Optional

from stocklake.core.base_pipeline import Pipeline
from stocklake.core.constants import DATA_DIR
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
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(Pipeline):
    def __init__(
        self,
        skip_download: bool = False,
        exchange: Optional[Exchange] = None,
        store_type: Optional[StoreType] = StoreType.LOCAL_ARTIFACT,
    ):
        self.exchange = exchange
        self.skip_download = skip_download

        if store_type not in StoreType.types():
            raise StockLoaderException(
                f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
            )
        self.store_type = store_type
        self.save_dir = os.path.join(DATA_DIR, "nasdaqapi")
        self.stdout = PrettyStdoutPrint()

    def run(self):
        logger.info("{} NASDAQ pipeline starts {}".format("=" * 30, "=" * 30))
        if self.exchange == Exchange.NASDAQ or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NASDAQ} symbols with nasdapapi")
            exchange_repo = LocalArtifactRepository(
                os.path.join(self.save_dir, Exchange.NASDAQ)
            )
            downloader = NASDAQSymbolsDataLoader(exchange_repo, "raw_data.json")
            if not self.skip_download:
                self.stdout.normal_message("- Downloading ...")
                downloader.download()
            else:
                self.stdout.warning_message("- Skip Downloading")

            preprocessor = NASDAQSymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()
            self.stdout.success_message(
                f"- Completed🐳. The artifact is saved to {preprocessor.artifact_path}"
            )

        if self.exchange == Exchange.NYSE or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NYSE} symbols with nasdapapi")
            exchange_repo = LocalArtifactRepository(
                os.path.join(self.save_dir, Exchange.NASDAQ)
            )
            downloader = NYSESymbolsDataLoader(exchange_repo, "raw_data.json")
            if not self.skip_download:
                self.stdout.normal_message("- Downloading ...")
                downloader.download()
            else:
                self.stdout.warning_message("- Skip Downloading")

            preprocessor = NYSESymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()
            self.stdout.success_message(
                f"- Completed🐳. The artifact is saved to {preprocessor.artifact_path}"
            )

        if self.exchange == Exchange.AMEX or self.exchange is None:
            self.stdout.step_start(f"{Exchange.AMEX} symbols with nasdapapi")
            exchange_repo = LocalArtifactRepository(
                os.path.join(self.save_dir, Exchange.NASDAQ)
            )
            downloader = AMEXSymbolsDataLoader(exchange_repo, "raw_data.json")
            if not self.skip_download:
                self.stdout.normal_message("- Downloading ...")
                downloader.download()
            else:
                self.stdout.warning_message("- Skip Downloading")

            preprocessor = AMEXSymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()
            self.stdout.success_message(
                f"- Completed🐳. The artifact is saved to {preprocessor.artifact_path}"
            )
