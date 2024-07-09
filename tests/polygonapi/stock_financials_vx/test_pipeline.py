import os

import pytest

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.stock_financials_vx.pipeline import (
    PolygonFinancialsDataPipeline,
)
from stocklake.polygonapi.stock_financials_vx.stores import SAVE_ARTIFACTS_DIR
from stocklake.stores.constants import StoreType
from stocklake.stores.db.models import PolygonFinancialsData
from tests.polygonapi.stock_financials_vx.test_data_loader import (
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F401
)


def test_invalid_store_type_specified():
    with pytest.raises(StockLakeException) as exc:
        _ = PolygonFinancialsDataPipeline(
            symbols=["AAPL"], store_type="INVALID_STORE_TYPE"
        )
        assert "Specified store type is invalid, INVALID_STORE_TYPE" in str(exc.value)


def test_run_with_local_artifact(MockPolygonStockFinancialsVxAPIServer):  # noqa: F811
    pipeline = PolygonFinancialsDataPipeline(
        symbols=["AAPL"],
        skip_download=False,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "financials_data.csv"))


def test_run_with_postgresql(
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,
):
    with SessionLocal() as session, session.begin():
        res = session.query(PolygonFinancialsData).all()
        assert len(res) == 0

    pipeline = PolygonFinancialsDataPipeline(
        symbols=["AAPL"],
        skip_download=False,
        store_type=StoreType.POSTGRESQL,
        sqlalchemy_session=SessionLocal,
    )
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(PolygonFinancialsData).all()
        assert len(res) > 0
