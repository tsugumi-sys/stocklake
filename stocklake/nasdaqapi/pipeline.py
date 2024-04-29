import logging
import os
from typing import Optional

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.base_preprocessor import BasePreprocessor
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
from stocklake.stores.artifact.base import ArtifactRepository
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.stores.constants import StoreType

logger = logging.getLogger(__name__)


class NASDAQSymbolsPipeline(BasePipeline):
    def __init__(
        self,
        skip_download: bool = False,
        exchange: Optional[Exchange] = None,
        store_type: Optional[StoreType] = StoreType.LOCAL_ARTIFACT,
        data_dir: str = DATA_DIR,
    ):
        self.exchange = exchange
        self.skip_download = skip_download

        if store_type not in StoreType.types():
            raise StockLoaderException(
                f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
            )
        self.store_type = store_type
        self._save_dir = os.path.join(data_dir, "nasdaqapi")
        self.stdout = PrettyStdoutPrint()

    @property
    def save_dir_path(self) -> str:
        return self._save_dir

    def run(self):
        logger.info("{} NASDAQ pipeline starts {}".format("=" * 30, "=" * 30))
        repository = LocalArtifactRepository(self._save_dir)

        if self.exchange == Exchange.NASDAQ or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NASDAQ} symbols with nasdapapi")
            data_loader = NASDAQSymbolsDataLoader(repository)
            preprocessor = NASDAQSymbolsPreprocessor(
                repository, data_loader.artifact_path
            )
            self._run(repository, data_loader, preprocessor)

        if self.exchange == Exchange.NYSE or self.exchange is None:
            self.stdout.step_start(f"{Exchange.NYSE} symbols with nasdapapi")
            data_loader = NYSESymbolsDataLoader(repository)
            preprocessor = NYSESymbolsPreprocessor(
                repository, data_loader.artifact_path
            )
            self._run(repository, data_loader, preprocessor)

        if self.exchange == Exchange.AMEX or self.exchange is None:
            self.stdout.step_start(f"{Exchange.AMEX} symbols with nasdapapi")
            data_loader = AMEXSymbolsDataLoader(repository)
            preprocessor = AMEXSymbolsPreprocessor(
                repository, data_loader.artifact_path
            )
            self._run(repository, data_loader, preprocessor)

    def _run(
        self,
        repository: ArtifactRepository,
        data_loader: BaseDataLoader,
        preprocessor: BasePreprocessor,
    ):
        if not self.skip_download:
            self.stdout.normal_message("- Downloading ...")
            data_loader.download()
        else:
            self.stdout.warning_message("- Skip Downloading")
        preprocessor.process()
        self.stdout.success_message(
            f"- Completed🐳. The artifact is saved to {self._save_dir}"
        )
