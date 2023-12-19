import logging
from typing import Optional

from stocklake.core.base_pipeline import Pipeline
from stocklake.core.stdout import PrettyStdoutPrint
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

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(Pipeline):
    def __init__(
        self, skip_download: bool = False, exchange: Optional[Exchange] = None
    ):
        self.exchange = exchange
        self.skip_download = skip_download
        self.stdout = PrettyStdoutPrint()

    def run(self):
        logger.info("{} NASDAQ pipline starts {}".format("=" * 30, "=" * 30))
        if self.exchange == Exchange.NASDAQ or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NASDAQ} symbols with nasdapapi")
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{Exchange.NASDAQ}")
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
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{Exchange.NYSE}")
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
            exchange_repo = LocalArtifactRepository(f"data/nasdaq/{Exchange.AMEX}")
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
