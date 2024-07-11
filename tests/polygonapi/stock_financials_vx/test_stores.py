import os

import pytest

from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.stock_financials_vx import entities
from stocklake.polygonapi.stock_financials_vx.data_loader import (
    PolygonFinancialsDataLoader,
)
from stocklake.polygonapi.stock_financials_vx.preprocessor import (
    PolygonFinancialsDataPreprocessor,
)
from stocklake.polygonapi.stock_financials_vx.stores import (
    SAVE_ARTIFACTS_DIR,
    PolygonFinancialsDataSQLAlchemyStore,
    PolygonFinancialsDataStore,
)
from stocklake.stores.constants import StoreType
from stocklake.stores.db import models
from tests.polygonapi.stock_financials_vx.test_data_loader import (
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F401
)


@pytest.fixture
def polygon_financials_data(
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F811
    monkeypatch,
):
    monkeypatch.setenv(STOCKLAKE_POLYGON_API_KEY.env_name, "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    preprocessor = PolygonFinancialsDataPreprocessor()
    data = preprocessor.process(dataloader.download(["AAPL"]))
    yield data


def test_polygon_financials_store_local_artifact(
    polygon_financials_data,
):
    store = PolygonFinancialsDataStore()
    store.save(StoreType.LOCAL_ARTIFACT, polygon_financials_data)
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "financials_data.csv"))


def test_polygon_financials_store_postgresql(
    SessionLocal,
    polygon_financials_data,
):
    store = PolygonFinancialsDataStore(SessionLocal)
    store.save(StoreType.POSTGRESQL, polygon_financials_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
    assert len(res) == 10


def test_PolygonFinancialsDataSQLAlchemyStore_create(
    polygon_financials_data,
    SessionLocal,
):
    data_length = len(polygon_financials_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
        assert len(res) == 0

    store = PolygonFinancialsDataSQLAlchemyStore(SessionLocal)
    store.create(
        [
            entities.PolygonFinancialsDataCreate(**d.model_dump())
            for d in polygon_financials_data
        ]
    )

    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
        assert len(res) == data_length


def test_PolygonFinancialsDataSQLAlchemyStore_delete(
    polygon_financials_data,
    SessionLocal,
):
    data_length = len(polygon_financials_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
        assert len(res) == 0

    store = PolygonFinancialsDataSQLAlchemyStore(SessionLocal)
    store.create(
        [
            entities.PolygonFinancialsDataCreate(**d.model_dump())
            for d in polygon_financials_data
        ]
    )

    # check data is created
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
        assert len(res) == data_length

    # delete all rows
    store.delete()

    # check successfully deleted.
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonFinancialsData).all()
        assert len(res) == 0