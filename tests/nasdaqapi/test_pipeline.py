import os
from unittest import mock

import pytest

from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline
from stocklake.nasdaqapi.stores import SAVE_ARTIFACTS_DIR
from stocklake.stores.constants import StoreType
from stocklake.stores.db.models import NasdaqApiData
from tests.nasdaqapi.test_data_loader import mock_requests_get
from tests.stores.db.utils import SessionLocal  # noqa: F401


def test_invalid_store_type_specified():
    with pytest.raises(StockLoaderException) as exc:
        _ = NASDAQSymbolsPipeline(store_type="INVALID_STORE_TYPE")
    assert (
        str(exc.value)
        == "Specified store type is invalid, INVALID_STORE_TYPE, valid types are ['local_artifact', 'postgresql']"
    )


@mock.patch("requests.get", side_effect=mock_requests_get)
@pytest.mark.parametrize("exchange_name", Exchange.exchanges())
def test_run_each_symbols_with_local_artifact(mock_get, exchange_name, tmpdir):
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        exchange=exchange_name,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, f"{exchange_name}_data.csv"))


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_run_with_local_artifact(mock_get, tmpdir):
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        store_type=StoreType.LOCAL_ARTIFACT,
    )
    pipeline.run()
    for exchange_name in Exchange.exchanges():
        assert os.path.exists(
            os.path.join(SAVE_ARTIFACTS_DIR, f"{exchange_name}_data.csv")
        )


@mock.patch("requests.get", side_effect=mock_requests_get)
@pytest.mark.parametrize("exchange", Exchange.exchanges())
def test_run_each_symbols_with_postgresql(
    mock_get,
    exchange,
    tmpdir,
    SessionLocal,  # noqa: F811
):
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        exchange=exchange,
        store_type=StoreType.POSTGRESQL,
        sqlalchemy_session=SessionLocal,
    )
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(NasdaqApiData).all()
        assert len(res) > 0


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_run_with_postgresql(mock_get, tmpdir, SessionLocal):  # noqa: F811
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        store_type=StoreType.POSTGRESQL,
        sqlalchemy_session=SessionLocal,
    )
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(NasdaqApiData).all()
        assert len(res) > 0
