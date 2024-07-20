import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars import cli
from stocklake.stores.constants import ArtifactFormat, StoreType
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


# MEMO: If a given `interval_sec` is not integer, click automatically check it and stdout error message (but not raise an exception).
@pytest.mark.parametrize("interval_sec", [-1])
def test_polygonapi_stock_financials_vx_invalid_interval_ms(interval_sec):
    runner = CliRunner()
    with pytest.raises((ValueError, Exception)):
        _ = runner.invoke(
            cli.aggregates_bars,
            [
                "--symbols",
                "AAPL",
                "--interval_sec",
                interval_sec,
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize("store_type", StoreType.types())
def test_polygonapi_aggregates_bars(
    store_type,
    MockPolygonAggregatesBarsAPIServer,  # noqa: F811
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


@pytest.mark.parametrize(
    "artifact_format", [None, ArtifactFormat.CSV, "INVALID_FORMAT"]
)
def test_polygonapi_aggregates_bars_local_artifact(
    artifact_format,
    MockPolygonAggregatesBarsAPIServer,  # noqa: F811
):
    runner = CliRunner()
    if artifact_format is None or artifact_format in ArtifactFormat.formats():
        res = runner.invoke(
            cli.aggregates_bars,
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
        assert "- Completed🐳" in res.output
    else:
        with pytest.raises(StockLakeException):
            _ = runner.invoke(
                cli.aggregates_bars,
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
