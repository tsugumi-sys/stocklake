import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi import cli
from stocklake.polygonapi.constants import PolygonAPIType
from stocklake.stores.constants import StoreType
from tests.polygonapi.test_data_loader import MockPolygonAPIServer  # noqa: F401
from tests.stores.db.utils import SessionLocal  # noqa: F401


def test_polygonapi_empty_symbols():
    runner = CliRunner()
    with pytest.raises(StockLakeException) as exc:
        _ = runner.invoke(
            cli.polygonapi,
            ["--api_type", PolygonAPIType.STOCK_FINANCIALS_VX],
            catch_exceptions=False,
        )
    assert str(exc.value) == "`symbols` must be given."


def test_polygonapi_api_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException) as exc:
        _ = runner.invoke(
            cli.polygonapi,
            ["--symbols", "AAPL", "--api_type", "INVALID_API_TYPE"],
            catch_exceptions=False,
        )
    assert (
        str(exc.value)
        == f"Invalid `api_type` INVALID_API_TYPE, supported type is {PolygonAPIType.types()}"
    )


def test_polygonapi_invalid_store_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.polygonapi,
            [
                "--symbols",
                "AAPL",
                "--api_type",
                "INVALID_API_TYPE",
                "--store_type",
                "INVALID_STORE_TYPE",
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize("store_type", StoreType.types())
def test_polygonapi_stock_financials_vx(
    store_type,
    MockPolygonAPIServer,  # noqa: F811
    monkeypatch,
    SessionLocal,  # noqa: F811
):
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    runner = CliRunner()
    res = runner.invoke(
        cli.polygonapi,
        [
            "--symbols",
            "AAPL",
            "--api_type",
            PolygonAPIType.STOCK_FINANCIALS_VX,
            "--store_type",
            store_type,
        ],
        catch_exceptions=False,
    )
    assert res.exit_code == 0
    assert "- Completed🐳" in res.output
