import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.stock_financials_vx import cli
from stocklake.stores.constants import ArtifactFormat, StoreType
from tests.polygonapi.stock_financials_vx.test_data_loader import (
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F401
)


def test_polygonapi_stock_financials_vx_empty_symbols():
    runner = CliRunner()
    with pytest.raises(StockLakeException) as exc:
        _ = runner.invoke(
            cli.stock_financials_vx,
            catch_exceptions=False,
        )
    assert str(exc.value) == "`symbols` must be given."


def test_polygonapi_stock_financials_vx_invalid_store_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.stock_financials_vx,
            [
                "--symbols",
                "AAPL",
                "--store_type",
                "INVALID_STORE_TYPE",
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize("store_type", StoreType.types())
def test_polygonapi_stock_financials_vx(
    store_type,
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F811
    SessionLocal,
):
    runner = CliRunner()
    res = runner.invoke(
        cli.stock_financials_vx,
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


@pytest.mark.parametrize(
    "artifact_format", [None, ArtifactFormat.CSV, "INVALID_FORMAT"]
)
def test_polygonapi_stock_financials_vx_local_artifact(
    artifact_format,
    MockPolygonStockFinancialsVxAPIServer,  # noqa: F811
):
    runner = CliRunner()
    if artifact_format in ArtifactFormat.formats() or artifact_format is None:
        res = runner.invoke(
            cli.stock_financials_vx,
            [
                "--symbols",
                "AAPL",
                "--store_type",
                "local_artifact",
                "--artifact_format",
                artifact_format,
            ],
            catch_exceptions=False,
        )
        assert res.exit_code == 0
    else:
        with pytest.raises(StockLakeException):
            _ = runner.invoke(
                cli.stock_financials_vx,
                [
                    "--symbols",
                    "AAPL",
                    "--store_type",
                    "local_artifact",
                    "--artifact_format",
                    artifact_format,
                ],
                catch_exceptions=False,
            )
