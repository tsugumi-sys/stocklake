import pytest

from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline


def test_invalid_store_type_specified():
    with pytest.raises(StockLoaderException) as exc:
        _ = NASDAQSymbolsPipeline(store_type="INVALID_STORE_TYPE")
    assert (
        str(exc.value)
        == "Specified store type is invalid, INVALID_STORE_TYPE, valid types are ['local_artifact', 'postgresql']"
    )
