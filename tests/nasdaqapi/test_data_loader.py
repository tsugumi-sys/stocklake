import json
import os
from unittest import mock

import pytest

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import NASDAQSymbolsDataLoader
from stocklake.nasdaqapi.entities import NasdaqAPIResponse

with open("./tests/nasdaqapi/sample_response.json") as f:
    mock_response: NasdaqAPIResponse = json.load(f)


def mock_requests_get(*args, **kwargs):
    class MockNasdaqAPIResponse:
        def __init__(
            self, json_data: NasdaqAPIResponse = mock_response, status_code: int = 200
        ):
            self._json_data = json_data
            self._status_code = status_code

        @property
        def status_code(self) -> int:
            return self._status_code

        def json(self) -> NasdaqAPIResponse:
            return self._json_data

    return MockNasdaqAPIResponse()


expected_cols = [
    "symbol",
    "name",
    "lastsale",
    "netchange",
    "pctchange",
    "marketCap",
    "url",
]


@mock.patch("requests.get", side_effect=mock_requests_get)
@pytest.mark.parametrize("exchange_name", Exchange.exchanges())
def test_data_loader(mock_get, exchange_name, tmpdir):
    data_loader = NASDAQSymbolsDataLoader(exchange_name=exchange_name, cache_dir=tmpdir)
    data = data_loader.download()
    assert os.path.exists(data_loader.cache_artifact_path)
    for row in data:
        for col in expected_cols:
            assert col in row
