from itertools import product

import pytest
from click.testing import CliRunner

from conftest import SessionLocal  # noqa: F401
from stocklake.exceptions import StockLakeException
from stocklake.nasdaqapi import cli
from stocklake.nasdaqapi.constants import Exchange
from stocklake.stores.constants import StoreType
from tests.nasdaqapi.test_data_loader import (
    MockNasdaqAPIServer,  # noqa: F401
)


def test_nasdaqapi_invalid_exchange():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.nasdaqapi, ["--exchange", "INVALID_EXCHANGE"], catch_exceptions=False
        )


def test_nasdaqapi_invalid_store_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.nasdaqapi,
            [
                "--store_type",
                "INVALID_STORE_TYPE",
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize(
    "exchange, store_type",
    list(product([None, *Exchange.exchanges()], StoreType.types())),
)
def test_nasdaqapi(
    exchange,
    store_type,
    MockNasdaqAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,  # noqa: F811
):
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    runner = CliRunner()
    res = runner.invoke(
        cli.nasdaqapi,
        [
            "--exchange",
            exchange,
            "--store_type",
            store_type,
        ],
        catch_exceptions=False,
    )
    assert res.exit_code == 0
    assert "- Completed🐳" in res.output
