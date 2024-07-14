import os

import pytest

from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.aggregates_bars.data_loader import (
    PolygonAggregatesBarsDataLoader,
)
from stocklake.polygonapi.aggregates_bars.preprocessor import (
    PolygonAggregatesBarsPreprocessor,
)
from stocklake.polygonapi.aggregates_bars.stores import (
    SAVE_ARTIFACTS_DIR,
    PolygonAggregatesBarsDataStore,
)
from stocklake.stores.constants import StoreType
from tests.polygonapi.aggregates_bars.test_data_loader import (
    MockPolygonAggregatesBarsAPIServer,  # noqa: F401
)


@pytest.fixture
def polygon_aggregates_bars_data(
    MockPolygonAggregatesBarsAPIServer,  # noqa: F811
    monkeypatch,
):
    monkeypatch.setenv(STOCKLAKE_POLYGON_API_KEY.env_name, "dummy_key")
    dataloader = PolygonAggregatesBarsDataLoader()
    preprocessor = PolygonAggregatesBarsPreprocessor()
    data = preprocessor.process(dataloader.download(["AAPL"]))
    yield data


def test_polygon_aggregates_bars_store_local_artifact(polygon_aggregates_bars_data):
    store = PolygonAggregatesBarsDataStore()
    store.save(StoreType.LOCAL_ARTIFACT, polygon_aggregates_bars_data)
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "aggregates_bars.csv"))
