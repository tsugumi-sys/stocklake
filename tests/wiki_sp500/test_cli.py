import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.stores.constants import StoreType
from stocklake.wiki_sp500 import cli


def test_wikisp500_invalid_store_type():
    runner = CliRunner()
    with pytest.raises(StockLakeException):
        _ = runner.invoke(
            cli.wikisp500,
            [
                "--store_type",
                "INVALID_STORE_TYPE",
            ],
            catch_exceptions=False,
        )


@pytest.mark.parametrize("store_type", StoreType.types())
def test_wikisp500_stock_financials_vx(
    store_type,
    SessionLocal,
):
    runner = CliRunner()
    res = runner.invoke(
        cli.wikisp500,
        [
            "--store_type",
            store_type,
        ],
        catch_exceptions=False,
    )
    assert res.exit_code == 0
    assert "- Completed🐳" in res.output
