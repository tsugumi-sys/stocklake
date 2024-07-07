import os

import pook
import pytest

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import NASDAQSymbolsDataLoader
from stocklake.nasdaqapi.utils import BASE_URL
from tests.mocks.mock_api_server import mock_responses


@pytest.fixture(scope="function")
def MockNasdaqAPIServer():
    pook.on()
    mock_resp = mock_responses(os.path.join(os.path.dirname(__file__), "mocks"))
    for mock in mock_resp:
        pook.get(BASE_URL + mock[0], reply=200, response_body=mock[1], times=10)
    yield MockNasdaqAPIServer
    pook.off()


expected_cols = [
    "symbol",
    "name",
    "lastsale",
    "netchange",
    "pctchange",
    "marketCap",
    "url",
]


@pytest.mark.parametrize("exchange_name", Exchange.exchanges())
def test_download(exchange_name, tmpdir, MockNasdaqAPIServer):
    data_loader = NASDAQSymbolsDataLoader(exchange_name=exchange_name, cache_dir=tmpdir)
    data = data_loader.download()
    assert os.path.exists(data_loader.cache_artifact_path)
    for d in data:
        for col in expected_cols:
            assert col in d.model_dump()
