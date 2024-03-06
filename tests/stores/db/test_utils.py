from click.testing import CliRunner

from stocklake.stores.db import cli
from tests.stores.db.utils import TEST_SQLALCHEMY_URL


def test_upgrade():
    runner = CliRunner()
    res = runner.invoke(
        cli.upgrade, ["--url", TEST_SQLALCHEMY_URL], catch_exceptions=False
    )
    assert res.exit_code == 0, res.output
