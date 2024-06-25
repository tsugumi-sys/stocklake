import os

import pook
import pytest
from polygon import RESTClient

from stocklake.exceptions import StockLoaderException
from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader
from tests.mocks.mock_api_server import mock_responses


@pytest.fixture(scope="function")
def MockPolygonAPIServer():
    pook.on()
    for mock in mock_responses(os.path.join(os.path.dirname(__file__), "mocks")):
        pook.get(
            RESTClient("").BASE + mock[0],
            reply=200,
            response_body=mock[1],
        )
    yield MockPolygonAPIServer


def test_raise_error_when_polygon_api_key_missing():
    with pytest.raises(StockLoaderException):
        _ = PolygonFinancialsDataLoader()


def test_download(MockPolygonAPIServer, monkeypatch):
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    dataloader = PolygonFinancialsDataLoader()
    res = dataloader.download(["AAPL"])
    assert "AAPL" in res
    assert len(res["AAPL"]) == 10
