import csv
import datetime
import hashlib
import logging
import os
from dataclasses import asdict
from typing import Dict, List, Optional

from polygon import RESTClient
from polygon.rest.models.aggs import Agg
from pydantic import BaseModel

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import (
    _STOCKLAKE_ENVIRONMENT,
    STOCKLAKE_POLYGON_API_KEY,
)
from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.utils import avoid_request_limit
from stocklake.polygonapi.validation import validate_polygonapi_api_key
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.utils.file_utils import save_data_to_csv

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "polygonapi_aggregates_bars")

logger = logging.getLogger(__name__)


class _ResponseMeta(BaseModel):
    ticker: str
    hash: str
    data: List[Agg]


class PolygonAggregatesBarsDataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH, use_cache: bool = False):
        super().__init__()
        validate_polygonapi_api_key()
        self._use_cache = use_cache
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filenames: List[str] = []
        self.polygon_client = RESTClient(STOCKLAKE_POLYGON_API_KEY.get())
        self.request_count_threshold = 5
        self.stdout = PrettyStdoutPrint()

    @property
    def cache_artifact_path(self):
        raise NotImplementedError()

    @property
    def cache_artifact_paths(self) -> List[str]:
        return [
            os.path.join(self._cache_artifact_repo.artifact_uri, f)
            for f in self._cache_artifact_filenames
        ]

    def download(
        self, tickers: List[str], from_: Optional[str] = None, to: Optional[str] = None
    ) -> Dict[str, List[Agg]]:
        if _STOCKLAKE_ENVIRONMENT.get() == "test":
            from_, to = "2023-01-09", "2023-02-10"
        if from_ is not None:
            validate_date_text(from_)
        else:
            from_ = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime(
                "%Y-%m-%d"
            )
        if to is not None:
            validate_date_text(from_)
        else:
            to = datetime.datetime.today().strftime("%Y-%m-%d")
        data = {}
        for request_count, ticker in enumerate(tickers):
            avoid_request_limit(
                self.request_count_threshold, request_count, self.stdout
            )
            metadata = self._request_agg_data(ticker, from_, to)
            # store to cache
            csv_file_name = f"{metadata.hash}.csv"
            save_data_to_csv(
                [asdict(d) for d in metadata.data],
                os.path.join(self._cache_artifact_repo.artifact_uri, csv_file_name),
            )
            self._cache_artifact_filenames.append(csv_file_name)
            data[ticker] = metadata.data
        return data

    def _request_agg_data(self, ticker: str, from_: str, to: str) -> _ResponseMeta:
        hash_key = stable_hash(f"{ticker}{from_}{to}")
        if self._use_cache:
            cache_file_path = os.path.join(
                self._cache_artifact_repo.artifact_uri, f"{hash_key}.csv"
            )
            if not os.path.exists(cache_file_path):
                raise StockLakeException(f"cached file not found, {cache_file_path}")
            with open(cache_file_path) as f:
                data = []
                for row in csv.DictReader(f):
                    _data = {}
                    for key, val in row.items():
                        if key in ["open", "high", "low", "close", "volume", "vwap"]:
                            _data[key] = float(val)
                        elif key in ["timestamp", "transactions"]:
                            _data[key] = int(val)
                        else:
                            _data[key] = bool(val) if val != "" else None  # type: ignore
                    data.append(_data)
            return _ResponseMeta(
                ticker=ticker, hash=hash_key, data=[Agg(**row) for row in data]
            )

        rawdata = []
        for d in self.polygon_client.list_aggs(
            ticker=ticker,
            multiplier=1,
            timespan="day",
            from_=from_,
            to=to,
            adjusted=True,
            sort="asc",
        ):
            rawdata.append(d)
        return _ResponseMeta(ticker=ticker, hash=hash_key, data=rawdata)


def validate_date_text(date_text: str):
    try:
        datetime.date.fromisoformat(date_text)
    except ValueError:
        raise ValueError(  # noqa: B904
            f"Incorrect data format, should be YYYY-MM-DD, but got {date_text}"
        )


def stable_hash(key: str) -> str:
    str_bytes = bytes(key, "UTF-8")
    m = hashlib.md5(str_bytes)
    return m.hexdigest()
