from stocklake.polygonapi.stock_financials_vx.data_loader import (
    PolygonFinancialsDataLoader,
)
from stocklake.polygonapi.stock_financials_vx.preprocessor import (
    PolygonFinancialsDataPreprocessor,
)
from tests.polygonapi.stock_financials_vx.test_data_loader import (
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F401
)


def test_preprocessor(MockPolygonStockFinancialsVxAPIServer):  # noqa: F811
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = dataloader.download(["AAPL"])
    data = preprocessor.process(data)
    assert len(data) == 10
    for d in data:
        for col, val in d.model_dump().items():
            if col in [
                "ticker",
                "start_date",
                "end_date",
                "cik",
                "company_name",
                "fiscal_period",
            ]:
                # check string data
                assert isinstance(val, str)
            elif col in [
                "filing_date",
                "source_filing_url",
                "source_filing_file_url",
            ]:
                assert isinstance(val, str) or val is None
            elif col in ["fiscal_year"]:
                assert isinstance(val, int) or val is None
            else:
                # check float data
                assert isinstance(val, float) or val is None
