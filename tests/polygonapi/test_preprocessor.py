from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from stocklake.polygonapi.preprocessor import PolygonFinancialsDataPreprocessor
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401


def test_preprocessor(MockPolygonAPIServer, monkeypatch):  # noqa: F811
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = preprocessor.process(dataloader.download(["MSFT"]))
    print(data)
