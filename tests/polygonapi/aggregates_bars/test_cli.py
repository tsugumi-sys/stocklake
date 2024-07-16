import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars import cli
from stocklake.stores.constants import StoreType
from tests.polygonapi.aggregates_bars.test_data_loader import (
    MockPolygonAggregatesBarsAPIServer,  # noqa: F401
)


def test_polygonapi_aggregates_bars_empty_symbols():
    runner = CliRunner()
    with pytest.raises(StockLakeException) as exc:
        _ = runner.invoke(
            cli.aggregates_bars,
            catch_exceptions=False,
        )
    assert str(exc.value) == "`symbols` must be given."


def test_polygonapi_aggregates_bars_invalid_store_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.aggregates_bars,
            [
                "--symbols",
                "AAPL",
                "--store_type",
                "INVALID_STORE_TYPE",
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize("store_type", StoreType.types())
def test_polygonapi_aggregates_bars(
    store_type,
    MockPolygonAggregatesBarsAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,
):
    runner = CliRunner()
    res = runner.invoke(
        cli.aggregates_bars,
        [
            "--symbols",
            "AAPL",
            "--store_type",
            store_type,
        ],
        catch_exceptions=False,
    )
    assert res.exit_code == 0
    assert "- Completed🐳" in res.output
