import logging
from typing import Dict, List

from polygon.rest.models.financials import StockFinancial

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.stores.db.schemas import PreprocessedPolygonFinancialsData

logger = logging.getLogger(__name__)


class PolygonFinancialsDataPreprocessor(BasePreprocessor):
    def process(
        self, data: Dict[str, List[StockFinancial]]
    ) -> List[PreprocessedPolygonFinancialsData]:
        processed_data: List[PreprocessedPolygonFinancialsData] = []
        for ticker, _data in data.items():
            ticker_financial_data = {}  # type: ignore
            ticker_financial_data["ticker"] = ticker
            for d in _data:
                ticker_financial_data["start_date"] = d.start_date
                ticker_financial_data["end_date"] = d.end_date
                ticker_financial_data["filing_date"] = d.filing_date
                ticker_financial_data["cik"] = d.cik
                ticker_financial_data["company_name"] = d.company_name
                ticker_financial_data["fiscal_period"] = d.fiscal_period
                ticker_financial_data["fiscal_year"] = d.fiscal_year
                ticker_financial_data["source_filing_url"] = d.source_filing_url
                ticker_financial_data["source_filing_file_url"] = (
                    d.source_filing_file_url
                )

                for base_name, financial_data in d.financials.__dict__.items():
                    if base_name not in [
                        "balance_sheet",
                        "cash_flow_statement",
                        "comprehensive_income",
                        "income_statement",
                    ]:
                        continue

                    if not isinstance(financial_data, dict):
                        financial_data = financial_data.__dict__
                    for financial_name, metadata in financial_data.items():
                        if metadata is None:
                            ticker_financial_data[financial_name] = None  # type: ignore
                            continue
                        ticker_financial_data[financial_name] = float(  # type: ignore
                            metadata.value * metadata.order
                        )
                    for field in PreprocessedPolygonFinancialsData.model_fields:
                        if field not in ticker_financial_data:
                            ticker_financial_data[field] = None  # type: ignore
            processed_data.append(
                PreprocessedPolygonFinancialsData(**ticker_financial_data)  # type: ignore
            )
        return processed_data
