import datetime
import logging
import os
from typing import Dict, List, Optional

from polygon import RESTClient
from polygon.rest.models.aggs import Agg

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import (
    _STOCKLAKE_ENVIRONMENT,
    STOCKLAKE_POLYGON_API_KEY,
)
from stocklake.polygonapi.utils import avoid_request_limit
from stocklake.polygonapi.validation import validate_polygonapi_api_key
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "polygonapi_aggregates_bars")

logger = logging.getLogger(__name__)


class PolygonAggregatesBarsDataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH, use_cache: bool = False):
        super().__init__()
        validate_polygonapi_api_key()
        self._use_cache = use_cache
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = "polygonapi_aggregates_bars.json"
        self.polygon_client = RESTClient(STOCKLAKE_POLYGON_API_KEY.get())
        self.request_count_threshold = 5
        self.stdout = PrettyStdoutPrint()

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_uri, self._cache_artifact_filename
        )

    def download(self, tickers: List[str]) -> Dict[str, List[Agg]]:
        data = {}
        for request_count, ticker in enumerate(tickers):
            avoid_request_limit(
                self.request_count_threshold, request_count, self.stdout
            )
            data[ticker] = self._request_agg_data(ticker)
        return data

    def _request_agg_data(
        self, ticker: str, from_: Optional[str] = None, to: Optional[str] = None
    ) -> List[Agg]:
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
        for date_text in [from_, to]:
            validate_date_text(date_text)
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
        return rawdata


def validate_date_text(date_text: str):
    try:
        datetime.date.fromisoformat(date_text)
    except ValueError:
        raise ValueError(  # noqa: B904
            f"Incorrect data format, should be YYYY-MM-DD, but got {date_text}"
        )
