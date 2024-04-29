# https://www.nasdaq.com/
import json
import logging
import os
import tempfile
from typing import List

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import RawNasdaqApiSymbolData
from stocklake.nasdaqapi.utils import nasdaq_api_get_request
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

logger = logging.getLogger(__name__)

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "nasdaqapi")


class NASDAQSymbolsDataLoader(BaseDataLoader):
    def __init__(self, exchange_name: Exchange, cache_dir: str = CACHE_DIR_PATH):
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = f"raw_{exchange_name}_data.json"
        self.exchange_name = exchange_name

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_dir, self._cache_artifact_filename
        )

    def download(self) -> List[RawNasdaqApiSymbolData]:
        logger.info(
            f"Loading {self.exchange_name.upper()} symbols data from `https://www.nasdaq.com/`"
        )
        res = nasdaq_api_get_request(self.exchange_name)
        data = res["data"]["rows"]
        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self._cache_artifact_filename)
            with open(local_file, "w") as f:
                json.dump(data, f)
            self._cache_artifact_repo.save_artifact(local_file)
        return data
