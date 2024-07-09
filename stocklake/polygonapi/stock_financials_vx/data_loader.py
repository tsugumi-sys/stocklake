import logging
import os
from typing import Dict, List

from polygon import RESTClient
from polygon.rest.models.financials import StockFinancial

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.utils import avoid_request_limit
from stocklake.polygonapi.validation import validate_polygonapi_api_key

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "polygonapi_finalcials")

logger = logging.getLogger(__name__)


class PolygonFinancialsDataLoader(BaseDataLoader):
    def __init__(self):
        super().__init__()
        validate_polygonapi_api_key()
        self.polygon_client = RESTClient(STOCKLAKE_POLYGON_API_KEY.get())
        self.filing_date_gte = "2022-01-01"
        self.request_count_threshold = 5
        self.stdout = PrettyStdoutPrint()

    @property
    def cache_artifact_path(self) -> str:
        return "dummy"

    def download(self, tickers: List[str]) -> Dict[str, List[StockFinancial]]:
        data = {}
        for request_count, ticker in enumerate(tickers):
            avoid_request_limit(
                self.request_count_threshold, request_count, self.stdout
            )
            data[ticker] = self._request_financials_data(ticker)
        return data

    def _request_financials_data(self, ticker: str) -> List[StockFinancial]:
        rawdata = []
        for d in self.polygon_client.vx.list_stock_financials(ticker=ticker, limit=100):
            rawdata.append(d)
        return rawdata
