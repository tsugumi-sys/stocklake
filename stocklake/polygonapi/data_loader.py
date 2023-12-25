import json
import logging
import os
import tempfile
import time
from typing import Any, Dict, Iterator, List

from dotenv import dotenv_values
from polygon import RESTClient
from polygon.rest.models.financials import Financials

from stocklake.data_loaders.base import DataLoader
from stocklake.data_loaders.common import RAW_DATA_DIR
from stocklake.stores.artifact.base import ArtifactRepository
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

logger = logging.getLogger(__name__)


class PolygonFinancialsDataLoader(DataLoader):
    def __init__(
        self,
        artifact_repo: ArtifactRepository = LocalArtifactRepository(
            os.path.join(RAW_DATA_DIR, "polygon/financials")
        ),
    ):
        super().__init__(artifact_repo)
        self.polygon_client = RESTClient(dotenv_values(".env").get("POLYGON_API_KEY"))
        self.filing_date_gte = "2022-01-01"
        self.request_limit_min = 5

    def download(self, tickers: List[str]):
        request_count = 0
        with tempfile.TemporaryDirectory() as tempdirname:
            for ticker in tickers:
                logger.info(f"Loading {ticker} data from Polygon ...")
                self._avoid_request_limit(request_count)
                request_count += 1

                financials_data = self._extract_data(
                    self._request_financials_data(ticker)
                )

                local_file = os.path.join(tempdirname, f"{ticker}_raw_data.json")
                with open(local_file, "w") as f:
                    json.dump(financials_data, f)
            self.artifact_repo.log_artifacts(tempdirname)

    def _extract_data(self, data: Iterator[Financials]) -> Dict[str, Any]:
        financials_data = {}
        for item in data:
            financial_data = {}
            financial_data["date"] = item.filing_date
            financial_data["fiscal_period"] = item.fiscal_period
            financial_data["fiscal_year"] = item.fiscal_year

            income_statement = item.financials.income_statement
            financial_data["revenues"] = {
                "formula": income_statement.revenues.formula,
                "label": income_statement.revenues.label,
                "order": income_statement.revenues.order,
                "unit": income_statement.revenues.unit,
                "value": income_statement.revenues.value,
                "xpath": income_statement.revenues.xpath,
            }

            financial_data["gross_profit"] = {
                "formula": income_statement.gross_profit.formula,
                "label": income_statement.gross_profit.label,
                "order": income_statement.gross_profit.order,
                "unit": income_statement.gross_profit.unit,
                "value": income_statement.gross_profit.value,
                "xpath": income_statement.gross_profit.xpath,
            }
            financials_data[item.filing_date] = financial_data
        return financials_data

    def _save_data(self, ticker: str, extracted_data: Dict[str, Any]):
        with open(os.path.join(self.save_dir_path, f"{ticker}.json"), "w") as f:
            json.dump(extracted_data, f)

    def _request_financials_data(self, ticker: str) -> Iterator[Financials]:
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
        logger.info("Waiting for 70 seconds to avoid request limit")
        time.sleep(70)
