# https://www.nasdaq.com/
import json
import logging
import os
import tempfile
from typing import List, TypedDict

import requests

from stocklake.core.base_data_loader import DataLoader
from stocklake.nasdaqapi.constants import Exchange
from stocklake.stores.artifact.base import ArtifactRepository

logger = logging.getLogger(__name__)


class _SymbolData(TypedDict):
    symbol: str
    name: str
    lastsale: str
    netchange: str
    pctchange: str
    marketCap: str
    url: str


class _ResponseData(TypedDict):
    asOf: str
    headers: _SymbolData
    rows: List[_SymbolData]


class NasdaqAPIResponse(TypedDict):
    data: _ResponseData


CUSTOM_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"
)
CUSTOM_HEADERS = {"user-agent": CUSTOM_USER_AGENT}


def symbols_api_endpoint(exchange_name: Exchange) -> str:
    return f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange_name}&download=true"


class NASDAQSymbolsDataLoader(DataLoader):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        artifact_filename_json: str = "data.json",
    ):
        super().__init__(artifact_repo)
        self.artifact_filename_json = artifact_filename_json
        self.exchange_name = Exchange.NASDAQ

    @property
    def artifact_path(self):
        return os.path.join(
            self.artifact_repo.artifact_dir, self.artifact_filename_json
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
            local_file = os.path.join(tempdirname, self.artifact_filename_json)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self.artifact_repo.save_artifact(local_file)


class NYSESymbolsDataLoader(DataLoader):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        artifact_filename_json: str = "data.json",
    ):
        super().__init__(artifact_repo)
        self.artifact_filename_json = artifact_filename_json
        self.exchange_name = Exchange.NYSE

    @property
    def artifact_path(self):
        return os.path.join(
            self.artifact_repo.artifact_dir, self.artifact_filename_json
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
            local_file = os.path.join(tempdirname, self.artifact_filename_json)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self.artifact_repo.save_artifact(local_file)


class AMEXSymbolsDataLoader(DataLoader):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        artifact_filename_json: str = "data.json",
    ):
        super().__init__(artifact_repo)
        self.artifact_filename_json = artifact_filename_json
        self.exchange_name = Exchange.AMEX

    @property
    def artifact_path(self):
        return os.path.join(
            self.artifact_repo.artifact_dir, self.artifact_filename_json
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
            local_file = os.path.join(tempdirname, self.artifact_filename_json)
            with open(local_file, "w") as f:
                json.dump(response_body["data"]["rows"], f)
            self.artifact_repo.save_artifact(local_file)
