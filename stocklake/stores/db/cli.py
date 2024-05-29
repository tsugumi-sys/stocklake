from typing import Optional

import click
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.engine.base import Engine

from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import (
    STOCKLAKE_POSTGRES_DATABASE,
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)
from stocklake.stores.db import utils


def _default_postgresql_url() -> str:
    return f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/{STOCKLAKE_POSTGRES_DATABASE.get()}"


def _is_db_connectable(engine: Engine, url: str, stdout: PrettyStdoutPrint) -> bool:
    try:
        conn = engine.connect()
        conn.close()
        return True
    except exc.OperationalError:
        stdout.warning_message(
            f"Cannot connect to database: {url}. You may forget to setup PostgreSQL, and see `Setup Database` section in the document (https://github.com/tsugumi-sys/stocklake/blob/main/README.md)."
        )
        return False


@click.command()
@click.option("--revision", default="head")
@click.option("--url", default=None)
def upgrade(revision: str, url: Optional[str] = None) -> None:
    if url is None:
        url = _default_postgresql_url()
    engine = sqlalchemy.create_engine(url)

    stdout = PrettyStdoutPrint()

    # check database is able to connect
    if not _is_db_connectable(engine, url, stdout):
        return

    utils.migrate(engine, revision)
    engine.dispose()
    stdout.success_message("Migration Completed :)")


@click.command()
@click.option("--message", default=None)
@click.option("--url", default=None)
def autogenerate_revision(message: str, url: Optional[str] = None):
    if url is None:
        url = _default_postgresql_url()
    engine = sqlalchemy.create_engine(url)
    stdout = PrettyStdoutPrint()
    # check database is connectable
    if not _is_db_connectable(engine, url, stdout):
        return

    utils.autogenerate_revision(engine, message)
    stdout.success_message("Auto generation of migration Completed :)")
