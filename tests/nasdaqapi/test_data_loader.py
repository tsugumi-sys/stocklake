import json
import os
import tempfile
from unittest import mock

from stocklake.nasdaqapi.data_loader import (
    AMEXSymbolsDataLoader,
    NasdaqAPIResponse,
    NASDAQSymbolsDataLoader,
    NYSESymbolsDataLoader,
)
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

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
def test_AMEXSymbolsDataLoader(mock_get):
    with tempfile.TemporaryDirectory() as tempdirpath:
        data_loader = AMEXSymbolsDataLoader(LocalArtifactRepository(tempdirpath))
        data_loader.download()
        assert os.path.exists(data_loader.artifact_path)


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_NasdaqAPIResponse(mock_get):
    with tempfile.TemporaryDirectory() as tempdirpath:
        data_loader = NASDAQSymbolsDataLoader(LocalArtifactRepository(tempdirpath))
        data_loader.download()
        assert os.path.exists(data_loader.artifact_path)


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_NYSESymbolsDataLoader(mock_get):
    with tempfile.TemporaryDirectory() as tempdirpath:
        data_loader = NYSESymbolsDataLoader(LocalArtifactRepository(tempdirpath))
        data_loader.download()
        assert os.path.exists(data_loader.artifact_path)
