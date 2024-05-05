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

    # def _extract_data(self, data: List[Financials]) -> Dict[str, Any]:
    #     financials_data = {}
    #     for item in data:
    #         financial_data = {}
    #         financial_data["date"] = item.filing_date
    #         financial_data["fiscal_period"] = item.fiscal_period
    #         financial_data["fiscal_year"] = item.fiscal_year

    #         income_statement = item.financials.income_statement
    #         financial_data["revenues"] = {
    #             "formula": income_statement.revenues.formula,
    #             "label": income_statement.revenues.label,
    #             "order": income_statement.revenues.order,
    #             "unit": income_statement.revenues.unit,
    #             "value": income_statement.revenues.value,
    #             "xpath": income_statement.revenues.xpath,
    #         }

    #         financial_data["gross_profit"] = {
    #             "formula": income_statement.gross_profit.formula,
    #             "label": income_statement.gross_profit.label,
    #             "order": income_statement.gross_profit.order,
    #             "unit": income_statement.gross_profit.unit,
    #             "value": income_statement.gross_profit.value,
    #             "xpath": income_statement.gross_profit.xpath,
    #         }
    #         financials_data[item.filing_date] = financial_data
    #     return financials_data

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
