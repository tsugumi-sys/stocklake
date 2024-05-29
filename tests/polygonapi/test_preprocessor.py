from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from stocklake.polygonapi.preprocessor import PolygonFinancialsDataPreprocessor
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401


def test_preprocessor(MockPolygonAPIServer, monkeypatch):  # noqa: F811
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = preprocessor.process(dataloader.download(["MSFT"]))
    for d in data:
        for col, val in d.items():
            if col in [
                "ticker",
                "start_date",
                "end_date",
                "filing_date",
                "cik",
                "company_name",
                "fiscal_period",
                "fiscal_year",
                "source_filing_url",
                "source_filing_file_url",
            ]:
                # check string data
                assert isinstance(val, str)
            else:
                print(col, val)
                # check float data
                assert isinstance(val, float)
