import logging
import os
import time
from typing import Dict, List

from polygon import RESTClient
from polygon.rest.models.financials import StockFinancial

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.validation import validate_polygonapi_api_key
from stocklake.utils.validation import validate_int_variable, validate_numeric_range

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "polygonapi_finalcials")

logger = logging.getLogger(__name__)


class PolygonFinancialsDataLoader(BaseDataLoader):
    def __init__(self, interval_sec: int = 0):
        super().__init__()
        validate_polygonapi_api_key()
        validate_int_variable(interval_sec, "timeout_sec")
        validate_numeric_range(interval_sec, "timeout_sec", min_=0)

        self.interval_sec = interval_sec
        self.polygon_client = RESTClient(STOCKLAKE_POLYGON_API_KEY.get())
        self.filing_date_gte = "2022-01-01"
        self.request_count_threshold = 5
        self.stdout = PrettyStdoutPrint()

    @property
    def cache_artifact_path(self) -> str:
        return "dummy"

    @property
    def cache_artifact_paths(self):
        raise NotImplementedError()

    def download(self, tickers: List[str]) -> Dict[str, List[StockFinancial]]:
        data = {}
        for ticker in tickers:
            data[ticker] = self._request_financials_data(ticker)
            if self.interval_sec > 0:
                self.stdout.normal_message(
                    f"waiting with an interval of {self.interval_sec} seconds"
                )
                time.sleep(self.interval_sec)
        return data

    def _request_financials_data(self, ticker: str) -> List[StockFinancial]:
        rawdata = []
        for d in self.polygon_client.vx.list_stock_financials(ticker=ticker, limit=100):
            rawdata.append(d)
        return rawdata
