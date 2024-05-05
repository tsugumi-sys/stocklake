import os
import re

import pook
import pytest
from polygon import RESTClient

from stocklake.exceptions import StockLoaderException
from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader

# mocking polygon api server. See https://github.com/polygon-io/client-python/blob/master/test_rest/base.py
polygonapi_mocks = []
dirname = os.path.dirname(__file__)
mockdir = os.path.join(dirname, "mocks")
for dname, _, files in os.walk(mockdir):
    for fname in files:
        if fname.endswith(".json"):
            abspath = os.path.join(dname, fname)
            with open(abspath) as f:
                urllpath = abspath.replace(mockdir, "").replace("\\", "/")
                urllpath = re.sub(".json$", "", urllpath)
                urllpath = re.sub("/index$", "", urllpath)
                # Windows will be sad. We support dev on Windows.
                if "?" in urllpath:
                    raise Exception(f"use & instead of ? in path ${urllpath}")
                urllpath = urllpath.replace("&", "?", 1)
                if ":" in urllpath:
                    raise Exception(f"use ; instead of : in path ${urllpath}")
                urllpath = urllpath.replace(";", ":", 1)
                # print(abspath, urllpath)
                polygonapi_mocks.append((urllpath, f.read()))


@pytest.fixture(scope="function")
def MockPolygonAPIServer():
    pook.on()
    for mock in polygonapi_mocks:
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
    res = dataloader.download(["MSFT"])
    assert "MSFT" in res
    assert len(res["MSFT"]) == 1
    assert res["MSFT"][0].cik == "0001413447"
