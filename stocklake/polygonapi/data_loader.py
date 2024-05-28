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
from stocklake.exceptions import StockLoaderException

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "polygonapi_finalcials")

logger = logging.getLogger(__name__)


class PolygonFinancialsDataLoader(BaseDataLoader):
    def __init__(self):
        super().__init__()
        if STOCKLAKE_POLYGON_API_KEY.get() is None:
            raise StockLoaderException(
                "You need to set an environment variable `STOCKLAKE_POLYGON_API_KEY`."
            )
        self.polygon_client = RESTClient(STOCKLAKE_POLYGON_API_KEY.get())
        self.filing_date_gte = "2022-01-01"
        self.request_limit_min = 5
        self.stdout = PrettyStdoutPrint()

    @property
    def cache_artifact_path(self) -> str:
        return "dummy"

    def download(self, tickers: List[str]) -> Dict[str, List[StockFinancial]]:
        data = {}
        for request_count, ticker in enumerate(tickers):
            logger.info(f"Loading {ticker} data from Polygon ...")
            self._avoid_request_limit(request_count)
            data[ticker] = self._request_financials_data(ticker)
        return data

    def _request_financials_data(self, ticker: str) -> List[StockFinancial]:
        rawdata = []
        for d in self.polygon_client.vx.list_stock_financials(
            ticker=ticker, filing_date_gte=self.filing_date_gte
        ):
            rawdata.append(d)
        return rawdata

    def _avoid_request_limit(self, request_count: int):
        if request_count < self.request_limit_min:
            return
        if request_count % 5 != 0:
            return
        self.stdout.normal_message("Waiting for 70 seconds to avoid request limit")
        time.sleep(70)
