import json
import logging
import os
from typing import Any, List, TypedDict

import pandas as pd

from stocklake.preprocessors.base import BasePreprocessor

logger = logging.getLogger(__name__)


class FinancialsTableData(TypedDict):
    ticker: List[Any]
    fiscal_period: List[Any]
    fiscal_year: List[Any]
    fiscal_date: List[Any]
    revenue: List[Any]
    gross_profit: List[Any]
    unit: List[Any]


class PolygonFinancialsDataPreprocessor(BasePreprocessor):
    def __init__(self, source_dir_path: str, save_dir: str = "polygon/financials/"):
        super().__init__(source_dir_path, save_dir)

    def preprocess(self, tickers: List[str]):
        data: FinancialsTableData = {
            "ticker": [],
            "fiscal_period": [],
            "fiscal_year": [],
            "fiscal_date": [],
            "revenue": [],
            "gross_profit": [],
            "unit": [],
        }
        for ticker in tickers:
            logger.info(f"Preprocessing {ticker} data ...")
            raw_data = self._load_data(ticker)
            for date, item in raw_data.items():
                logger.debug(f"{'=' * 20} {date} {'=' * 20}")
                logger.debug("Fiscal Period: {}".format(item.get("fiscal_period")))
                logger.debug("Fiscal Year: {}".format(item.get("fiscal_year")))
                # Calculate revenue
                if item.get("revenues").get("formula") is not None:
                    logger.warning(
                        "formula exists on revenues: {}".format(
                            item.get("revenues").get("formula")
                        )
                    )
                logger.debug(
                    "Revenue: {} {}".format(
                        item.get("revenues").get("value"),
                        item.get("revenues").get("unit"),
                    )
                )
                # Calculate gross profit
                if item.get("gross_profit").get("formula") is not None:
                    logger.warning(
                        "formula exists on gross profit: {}".format(
                            item.get("gross_profit").get("formula")
                        )
                    )
                logger.debug(
                    "Revenue: {} {}".format(
                        item.get("gross_profit").get("value"),
                        item.get("gross_profit").get("unit"),
                    )
                )

                data["ticker"].append(ticker)
                data["fiscal_period"].append(item.get("fiscal_period"))
                data["fiscal_year"].append(item.get("fiscal_year"))
                data["fiscal_date"].append(date)
                data["revenue"].append(item.get("revenues").get("value"))
                data["gross_profit"].append(item.get("gross_profit").get("value"))
                data["unit"].append(item.get("revenues").get("unit"))

        pd.DataFrame.from_dict(data).to_csv(
            os.path.join(self.save_dir_path, "financials.csv")
        )

    def _load_data(self, ticker: str) -> dict:
        with open(os.path.join(self.source_dir_path, f"{ticker}.json")) as f:
            data = json.load(f)
        return data
