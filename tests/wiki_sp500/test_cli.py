import pytest
from click.testing import CliRunner

from stocklake.exceptions import StockLakeException
from stocklake.stores.constants import ArtifactFormat, StoreType
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
def test_wikisp500(
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


@pytest.mark.parametrize(
    "artifact_format", [None, ArtifactFormat.CSV, "INVALID_FORMAT"]
)
def test_wikisp500_local_artifact(artifact_format):
    runner = CliRunner()
    if artifact_format in ArtifactFormat.formats() or artifact_format is None:
        res = runner.invoke(
            cli.wikisp500,
            ["--store_type", "local_artifact", "--artifact_format", artifact_format],
            catch_exceptions=False,
        )
        assert res.exit_code == 0
    else:
        with pytest.raises(StockLakeException):
            _ = runner.invoke(
                cli.wikisp500,
                [
                    "--store_type",
                    "local_artifact",
                    "--artifact_format",
                    artifact_format,
                ],
                catch_exceptions=False,
            )
