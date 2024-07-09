import os

import pook
import pytest
from polygon import RESTClient

from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from tests.mocks.mock_api_server import mock_responses


@pytest.fixture(scope="function")
def MockPolygonAggregatesBarsAPIServer():
    pook.on()
    for mock in mock_responses(os.path.join(os.path.dirname(__file__), "mocks")):
        url = "/" + os.path.join(*mock[0].split("/")[:-1])
        pook.get(
            RESTClient("").BASE + url,
            reply=200,
            response_body=mock[1],
        )
    yield MockPolygonAggregatesBarsAPIServer
    pook.off()


def test_download(MockPolygonAggregatesBarsAPIServer, monkeypatch):
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    res = RESTClient(STOCKLAKE_POLYGON_API_KEY.get()).list_aggs(
        ticker="AAPL",
        multiplier=1,
        timespan="day",
        from_="2023-01-09",
        to="2023-02-10",
        adjusted=True,
        sort="asc",
    )
    for a in res:
        print(a)
