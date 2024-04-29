import os
from unittest import mock

import pytest

from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline
from stocklake.stores.constants import StoreType
from tests.nasdaqapi.test_data_loader import mock_requests_get


def test_invalid_store_type_specified():
    with pytest.raises(StockLoaderException) as exc:
        _ = NASDAQSymbolsPipeline(store_type="INVALID_STORE_TYPE")
    assert (
        str(exc.value)
        == "Specified store type is invalid, INVALID_STORE_TYPE, valid types are ['local_artifact', 'postgresql']"
    )


@mock.patch("requests.get", side_effect=mock_requests_get)
@pytest.mark.parametrize("exchange_name", Exchange.exchanges())
def test_run_each_symbols_with_local_artifact(mock_get, exchange_name, tmpdir):
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        exchange=exchange_name,
        store_type=StoreType.LOCAL_ARTIFACT,
        data_dir=tmpdir,
    )
    pipeline.run()
    data_dir = os.path.join(pipeline.save_dir_path, "nasdaq")
    assert os.path.exists(os.path.join(data_dir, f"{exchange_name}_data.csv"))
    assert os.path.exists(os.path.join(data_dir, f"raw_{exchange_name}_data.json"))


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_run_with_local_artifact(mock_get, tmpdir):
    pipeline = NASDAQSymbolsPipeline(
        skip_download=False,
        store_type=StoreType.LOCAL_ARTIFACT,
        data_dir=tmpdir,
    )
    pipeline.run()
    data_dir = os.path.join(pipeline.save_dir_path, "nasdaq")
    for exchange_name in Exchange.exchanges():
        assert os.path.exists(os.path.join(data_dir, f"{exchange_name}_data.csv"))
        assert os.path.exists(os.path.join(data_dir, f"raw_{exchange_name}_data.json"))