# https://www.nasdaq.com/
import json
import logging
import os
import tempfile
from typing import List, TypedDict

import requests

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqApiSymbolData
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

logger = logging.getLogger(__name__)

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "nasdaqapi")


class _ResponseData(TypedDict):
    asOf: str
    headers: NasdaqApiSymbolData
    rows: List[NasdaqApiSymbolData]


class NasdaqAPIResponse(TypedDict):
    data: _ResponseData


CUSTOM_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"
)
CUSTOM_HEADERS = {"user-agent": CUSTOM_USER_AGENT}


def symbols_api_endpoint(exchange_name: Exchange) -> str:
    return f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange_name}&download=true"


class NASDAQSymbolsDataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH):
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = "raw_nasdaq_data.json"
        self.exchange_name = Exchange.NASDAQ

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_dir, self._cache_artifact_filename
        )

    def download(self):
        logger.info(
            f"Loading {self.exchange_name.upper()} symbols data from `https://www.nasdaq.com/`"
        )

        res = requests.get(
            symbols_api_endpoint(self.exchange_name), headers=CUSTOM_HEADERS
        )
        if res.status_code != 200:
            logger.error(
                f"Request Failed with status code: {res.status_code}. All response body is the following: {res.text}"
            )
            return

        response_body: NasdaqAPIResponse = res.json()

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self._cache_artifact_filename)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self._cache_artifact_repo.save_artifact(local_file)


class NYSESymbolsDataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH):
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = "raw_nyse_data.json"
        self.exchange_name = Exchange.NYSE

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_dir, self._cache_artifact_filename
        )

    def download(self):
        logger.info(
            f"Loading {self.exchange_name.upper()} symbols data from `https://www.nasdaq.com/`"
        )
        res = requests.get(
            symbols_api_endpoint(self.exchange_name), headers=CUSTOM_HEADERS
        )

        if res.status_code != 200:
            logger.error(
                f"Request Failed with status code: {res.status_code}. All response body is the following: {res.text}"
            )

        response_body: NasdaqAPIResponse = res.json()

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self._cache_artifact_filename)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self._cache_artifact_repo.save_artifact(local_file)


class AMEXSymbolsDataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH):
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = "raw_amex_data.json"

        self.exchange_name = Exchange.AMEX

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_dir, self._cache_artifact_filename
        )

    def download(self):
        logger.info(
            f"Loading {self.exchange_name.upper()} symbols data from `https://www.nasdaq.com/`"
        )

        res = requests.get(
            symbols_api_endpoint(self.exchange_name), headers=CUSTOM_HEADERS
        )

        if res.status_code != 200:
            logger.error(
                f"Request Failed with status code: {res.status_code}. All response body is the following: {res.text}"
            )

        response_body: NasdaqAPIResponse = res.json()

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self._cache_artifact_filename)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self._cache_artifact_repo.save_artifact(local_file)
