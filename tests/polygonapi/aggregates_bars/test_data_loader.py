import os
from unittest import mock

import pook
import pytest
from polygon import RESTClient

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars.data_loader import (
    PolygonAggregatesBarsDataLoader,
)
from tests.mocks.mock_api_server import mock_responses


@pytest.fixture(scope="function")
def MockPolygonAggregatesBarsAPIServer():
    pook.on()
    for resp in mock_responses(os.path.join(os.path.dirname(__file__), "mocks")):
        url = "/" + os.path.join(*resp[0].split("/")[:-1])
        pook.get(
            RESTClient("").BASE + url,
            reply=200,
            response_body=resp[1],
        )
    yield MockPolygonAggregatesBarsAPIServer
    pook.off()


def test_raise_error_when_polygon_api_key_missing():
    with mock.patch.dict(os.environ, clear=True), pytest.raises(StockLakeException):
        _ = PolygonAggregatesBarsDataLoader()


@pytest.mark.parametrize("interval_sec", [-1, "a"])
def test_invalid_interval_sec(interval_sec):
    with pytest.raises(ValueError):
        _ = PolygonAggregatesBarsDataLoader(interval_sec=interval_sec)


@pytest.mark.parametrize("use_cache", [False, True])
def test_download(use_cache, MockPolygonAggregatesBarsAPIServer):
    data_loader = PolygonAggregatesBarsDataLoader(use_cache=use_cache)
    res = data_loader.download(["AAPL"])
    assert "AAPL" in res
    assert len(res["AAPL"]) == 24
