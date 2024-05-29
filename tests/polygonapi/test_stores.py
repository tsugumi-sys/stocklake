import os

from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from stocklake.polygonapi.preprocessor import PolygonFinancialsDataPreprocessor
from stocklake.polygonapi.stores import SAVE_ARTIFACTS_DIR, PolygonFinancialsDataStore
from stocklake.stores.constants import StoreType
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401


def test_polygon_financials_store_local_artifact(
    MockPolygonAPIServer,  # noqa: F811
    monkeypatch,
):
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = preprocessor.process(dataloader.download(["MSFT"]))
    store = PolygonFinancialsDataStore()
    store.save(StoreType.LOCAL_ARTIFACT, data)
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "financials_data.csv"))
