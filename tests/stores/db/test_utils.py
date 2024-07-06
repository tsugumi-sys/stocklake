import pytest
from click.testing import CliRunner

from conftest import SessionLocal  # noqa: F401
from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.stores.db import cli
from stocklake.stores.db.database import database_url


@pytest.mark.usefixtures("test_database")
def test_upgrade(monkeypatch):
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    runner = CliRunner()
    res = runner.invoke(cli.upgrade, ["--url", database_url()], catch_exceptions=False)
    assert res.exit_code == 0
    assert "Migration Completed :)" in res.output


def test_upgrade_database_not_found():
    runner = CliRunner()
    res = runner.invoke(
        cli.upgrade, ["--url", "postgresql://invalid:1111"], catch_exceptions=False
    )
    assert res.exit_code == 0
    assert res.output == "{}{}{}{}{}".format(
        PrettyStdoutPrint.msg_colors.get("WARNING"),
        PrettyStdoutPrint.two_blank_spaces,
        "Cannot connect to database: postgresql://invalid:1111. You may forget to setup PostgreSQL, and see `Setup Database` section in the document (https://github.com/tsugumi-sys/stocklake/blob/main/README.md).",
        PrettyStdoutPrint.msg_colors.get("DEFAULT"),
        "\n",
    )


@pytest.mark.usefixtures("test_database")
def test_revision(monkeypatch):  # noqa: F811
    # set environment as test (to mock alembic script location)
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    runner = CliRunner()
    # you need to sync the current latest migration first.
    _ = runner.invoke(cli.upgrade, ["--url", database_url()], catch_exceptions=False)
    # autogenerate revision file
    revision_message = "Auto generate Test Revision"
    res = runner.invoke(
        cli.autogenerate_revision,
        ["--message", revision_message, "--url", database_url()],
    )
    assert res.exit_code == 0
    assert "Auto generation of migration Completed :)" in res.output
