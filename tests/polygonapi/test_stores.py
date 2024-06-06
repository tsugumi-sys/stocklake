import os

import pytest

from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from stocklake.polygonapi.preprocessor import PolygonFinancialsDataPreprocessor
from stocklake.polygonapi.stores import (
    SAVE_ARTIFACTS_DIR,
    PolygonFinancialsDataSQLAlchemyStore,
    PolygonFinancialsDataStore,
)
from stocklake.stores.constants import StoreType
from stocklake.stores.db import schemas
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401
from tests.stores.db.utils import SessionLocal  # noqa: F401


@pytest.fixture
def polygon_financials_data(
    MockPolygonAPIServer,  # noqa: F811
    monkeypatch,
):
    monkeypatch.setenv(STOCKLAKE_POLYGON_API_KEY.env_name, "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = preprocessor.process(dataloader.download(["MSFT"]))
    yield data


def test_polygon_financials_store_local_artifact(
    polygon_financials_data,
):
    store = PolygonFinancialsDataStore()
    store.save(StoreType.LOCAL_ARTIFACT, polygon_financials_data)
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "financials_data.csv"))


def test_PolygonFinancialsDataSQLAlchemyStore_create(
    polygon_financials_data,
    SessionLocal,  # noqa: F811
):
    store = PolygonFinancialsDataSQLAlchemyStore(SessionLocal)
    store.create(
        [
            schemas.PolygonFinancialsDataCreate(**d.dict())
            for d in polygon_financials_data
        ]
    )
