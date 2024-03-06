from typing import Optional

import click
import sqlalchemy

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
    engine = sqlalchemy.create_engine(
        f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/{STOCKLAKE_POSTGRES_DATABASE.get()}"
    )
    utils.migrate(engine, revision)
    engine.dispose()
