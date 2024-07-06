from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from stocklake.polygonapi.preprocessor import PolygonFinancialsDataPreprocessor
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401


def test_preprocessor(MockPolygonAPIServer, monkeypatch):  # noqa: F811
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
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
