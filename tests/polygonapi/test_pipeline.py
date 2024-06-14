import os

import pytest

from stocklake.exceptions import StockLoaderException
from stocklake.polygonapi.pipeline import PolygonFinancialsDataPipeline
from stocklake.polygonapi.stores import SAVE_ARTIFACTS_DIR
from stocklake.stores.constants import StoreType
from stocklake.stores.db.models import PolygonFinancialsData
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401
from tests.stores.db.utils import SessionLocal  # noqa: F401


def test_invalid_store_type_specified():
    with pytest.raises(StockLoaderException) as exc:
        _ = PolygonFinancialsDataPipeline(
            symbols=["MSFT"], store_type="INVALID_STORE_TYPE"
        )
        assert (
            str(exc.value)
            == "Specified store type is invalid, INVALID_STORE_TYPE, valid types are ['local_artifact', 'postgresql']"
        )


def test_run_with_local_artifact(MockPolygonAPIServer, monkeypatch):  # noqa: F811
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    pipeline = PolygonFinancialsDataPipeline(
        symbols=["MSFT"],
        skip_download=False,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "financials_data.csv"))


def test_run_with_postgresql(
    MockPolygonAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,  # noqa: F811
):
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    pipeline = PolygonFinancialsDataPipeline(
        symbols=["MSFT"],
        skip_download=False,
        store_type=StoreType.POSTGRESQL,
        sqlalchemy_session=SessionLocal,
    )
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(PolygonFinancialsData).all()
        assert len(res) > 0
