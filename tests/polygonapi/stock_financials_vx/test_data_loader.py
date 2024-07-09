import os
from unittest import mock

import pook
import pytest
from polygon import RESTClient

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.stock_financials_vx.data_loader import (
    PolygonFinancialsDataLoader,
)
from tests.mocks.mock_api_server import mock_responses


@pytest.fixture(scope="function")
def MockPolygonStockFinancialsVxAPIServer():
    pook.on()
    for resp in mock_responses(os.path.join(os.path.dirname(__file__), "mocks")):
        pook.get(
            RESTClient("").BASE + resp[0],
            reply=200,
            response_body=resp[1],
        )
    yield MockPolygonStockFinancialsVxAPIServer
    pook.off()


def test_raise_error_when_polygon_api_key_missing():
    with mock.patch.dict(os.environ, clear=True), pytest.raises(StockLakeException):
        _ = PolygonFinancialsDataLoader()


def test_download(MockPolygonStockFinancialsVxAPIServer):
    dataloader = PolygonFinancialsDataLoader()
    res = dataloader.download(["AAPL"])
    assert "AAPL" in res
    assert len(res["AAPL"]) == 10
