import pytest

from stocklake.exceptions import StockLoaderException
from stocklake.polygonapi.data_loader import PolygonFinancialsDataLoader


def test_raise_error_when_polygon_api_key_missing():
    with pytest.raises(StockLoaderException):
        _ = PolygonFinancialsDataLoader()
