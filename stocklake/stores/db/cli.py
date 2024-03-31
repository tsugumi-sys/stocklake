from typing import Optional

import click
import sqlalchemy
from sqlalchemy import exc

from stocklake.core.stdout import PrettyStdoutPrint
from stocklake.environment_variables import (
    STOCKLAKE_POSTGRES_DATABASE,
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)
from stocklake.stores.db import utils


@click.command()
@click.option("--url", default=None)
@click.option("--revision", default="head")
def upgrade(url: Optional[str], revision: str) -> None:
    if url is None:
        url = f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/{STOCKLAKE_POSTGRES_DATABASE.get()}"
    engine = sqlalchemy.create_engine(url)

    # test connection
    try:
        conn = engine.connect()
        conn.close()
    except exc.OperationalError:
        PrettyStdoutPrint().warning_message(
            f"Cannot connect to database: {url}. You may forget to setup PostgreSQL, and see `Setup Database` section in the document (https://github.com/tsugumi-sys/stocklake/blob/main/README.md)."
        )
        return

    utils.migrate(engine, revision)
    engine.dispose()
