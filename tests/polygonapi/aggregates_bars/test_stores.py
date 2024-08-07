import os

import pytest

from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.polygonapi.aggregates_bars import entities
from stocklake.polygonapi.aggregates_bars.data_loader import (
    PolygonAggregatesBarsDataLoader,
)
from stocklake.polygonapi.aggregates_bars.preprocessor import (
    PolygonAggregatesBarsPreprocessor,
)
from stocklake.polygonapi.aggregates_bars.stores import (
    SAVE_ARTIFACTS_DIR,
    PolygonAggregatesBarsDataSQLAlchemyStore,
    PolygonAggregatesBarsDataStore,
)
from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.stores.db import models
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


@pytest.mark.parametrize(
    "artifact_format", [None, ArtifactFormat.CSV, "INVALID_FORMAT"]
)
def test_polygon_aggregates_bars_store_local_artifact(
    artifact_format, polygon_aggregates_bars_data
):
    store = PolygonAggregatesBarsDataStore()
    if artifact_format is None or artifact_format in ArtifactFormat.formats():
        store.save(
            StoreType.LOCAL_ARTIFACT, polygon_aggregates_bars_data, artifact_format
        )
        assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "aggregates_bars.csv"))
    else:
        with pytest.raises(NotImplementedError):
            store.save(
                StoreType.LOCAL_ARTIFACT, polygon_aggregates_bars_data, artifact_format
            )


def test_polygon_financials_store_postgresql(
    SessionLocal,
    polygon_aggregates_bars_data,
):
    store = PolygonAggregatesBarsDataStore(SessionLocal)
    store.save(StoreType.POSTGRESQL, polygon_aggregates_bars_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
    assert len(res) == len(polygon_aggregates_bars_data)


def test_PolygonFinancialsDataSQLAlchemyStore_create(
    polygon_aggregates_bars_data,
    SessionLocal,
):
    data_length = len(polygon_aggregates_bars_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == 0

    store = PolygonAggregatesBarsDataSQLAlchemyStore(SessionLocal)
    store.create(
        [
            entities.PolygonAggregatesBarsDataCreate(**d.model_dump())
            for d in polygon_aggregates_bars_data
        ]
    )

    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == data_length


def test_PolygonFinancialsDataSQLAlchemyStore_delete(
    polygon_aggregates_bars_data,
    SessionLocal,
):
    data_length = len(polygon_aggregates_bars_data)
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == 0

    store = PolygonAggregatesBarsDataSQLAlchemyStore(SessionLocal)
    data = [
        entities.PolygonAggregatesBarsDataCreate(**d.model_dump())
        for d in polygon_aggregates_bars_data
    ]
    store.create(data)

    # check data is created
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == data_length

    # delete all rows
    store.delete()

    # check successfully deleted.
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == 0

    # create multi ticker data
    store.create(data)
    for d in data:
        d.ticker = "MSFT"
    store.create(data)

    # check successfully created
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == data_length * 2

    # delete MSFT data
    store.delete(["MSFT"])
    with SessionLocal() as session, session.begin():
        res = session.query(models.PolygonAggregatesBarsData).all()
        assert len(res) == data_length
        assert res[0].ticker == "AAPL"
