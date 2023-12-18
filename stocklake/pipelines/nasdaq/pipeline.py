import logging
from typing import Optional

from stocklake.data_loaders.nasdaq.data_loader import (
    AMEXSymbolsDataLoader,
    NASDAQSymbolsDataLoader,
    NYSESymbolsDataLoader,
)
from stocklake.pipelines.base import Pipeline
from stocklake.preprocessors.nasdaq.preprocessor import (
    AMEXSymbolsPreprocessor,
    NASDAQSymbolsPreprocessor,
    NYSESymbolsPreprocessor,
)
from stocklake.stores.artifact.base import LocalArtifactRepository
from stocklake.pipelines.nasdaq.constants import Exchange

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(Pipeline):
    def __init__(
        self, skip_download: bool = False, exchange: Optional[Exchange] = None
    ):
        self.exchange = exchange
        self.skip_download = skip_download

    def run(self):
        logger.info("{} NASDAQ pipline starts {}".format("=" * 30, "=" * 30))
        if self.exchange == Exchange.NASDAQ or self.exchange is None:
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{self.exchange}")
            downloader = NASDAQSymbolsDataLoader(exchange_repo, "raw_data.json")
            if not self.skip_download:
                downloader.download()

            preprocessor = NASDAQSymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()

        if self.exchange == Exchange.NYSE or self.exchange is None:
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{self.exchange}")
            downloader = NYSESymbolsDataLoader(exchange_repo, "raw_data.json")
            if not self.skip_download:
                downloader.download()

            preprocessor = NYSESymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()

        if self.exchange == Exchange.AMEX or self.exchange is None:
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{self.exchange}")
            downloader = AMEXSymbolsDataLoader(exchange_repo, "raw_data.json")
            if self.skip_download:
                downloader.download()

            preprocessor = AMEXSymbolsPreprocessor(
                exchange_repo, downloader.artifact_path, "processed.csv"
            )
            preprocessor.process()
