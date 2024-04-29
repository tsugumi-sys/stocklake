import json
import os
from unittest import mock

from stocklake.nasdaqapi.data_loader import (
    AMEXSymbolsDataLoader,
    NasdaqAPIResponse,
    NASDAQSymbolsDataLoader,
    NYSESymbolsDataLoader,
)

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


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_AMEXSymbolsDataLoader(mock_get, tmpdir):
    data_loader = AMEXSymbolsDataLoader(cache_dir=tmpdir)
    data_loader.download()
    assert os.path.exists(data_loader.cache_artifact_path)


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_NASDAQSymbolsDataLoader(mock_get, tmpdir):
    data_loader = NASDAQSymbolsDataLoader(cache_dir=tmpdir)
    data_loader.download()
    assert os.path.exists(data_loader.cache_artifact_path)


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_NYSESymbolsDataLoader(mock_get, tmpdir):
    data_loader = NYSESymbolsDataLoader(cache_dir=tmpdir)
    data_loader.download()
    assert os.path.exists(data_loader.cache_artifact_path)
