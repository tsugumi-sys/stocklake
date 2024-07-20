import os

import pytest

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars.pipeline import (
    PolygonAggregatesBarsDataPipeline,
)
from stocklake.polygonapi.aggregates_bars.stores import SAVE_ARTIFACTS_DIR
from stocklake.stores.constants import StoreType
from stocklake.stores.db.models import PolygonAggregatesBarsData
from tests.polygonapi.aggregates_bars.test_data_loader import (
    MockPolygonAggregatesBarsAPIServer,  # noqa: F401
)


def test_invalid_store_type_specified():
    with pytest.raises(StockLakeException) as exc:
        _ = PolygonAggregatesBarsDataPipeline(
            symbols=["AAPL"], store_type="INVALID_STORE_TYPE"
        )
        assert "Specified store type is invalid, INVALID_STORE_TYPE" in str(exc.value)


@pytest.mark.parametrize("interval_sec", [-1, "a"])
def test_invalid_interval_sec(interval_sec):
    with pytest.raises(ValueError):
        _ = PolygonAggregatesBarsDataPipeline(
            symbols=["AAPL"], interval_sec=interval_sec
        )


def test_run_with_local_artifact(MockPolygonAggregatesBarsAPIServer):  # noqa: F811
    pipeline = PolygonAggregatesBarsDataPipeline(
        symbols=["AAPL"],
        skip_download=False,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "aggregates_bars.csv"))

    # use cache
    pipeline = PolygonAggregatesBarsDataPipeline(
        symbols=["AAPL"],
        skip_download=True,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "aggregates_bars.csv"))


def test_run_with_postgresql(
    MockPolygonAggregatesBarsAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,
):
    with SessionLocal() as session, session.begin():
        res = session.query(PolygonAggregatesBarsData).all()
        assert len(res) == 0

    pipeline = PolygonAggregatesBarsDataPipeline(
        symbols=["AAPL"],
        skip_download=False,
        store_type=StoreType.POSTGRESQL,
        sqlalchemy_session=SessionLocal,
    )
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(PolygonAggregatesBarsData).all()
        assert len(res) > 0
