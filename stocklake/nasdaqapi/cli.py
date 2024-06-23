from typing import Optional

import click

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline
from stocklake.stores.constants import StoreType


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
)
@click.option(
    "--exchange",
    default=None,
    help=f"The exchange name that you want to download, should be in `{Exchange.exchanges()}`.",
)
@click.option(
    "--store_type",
    default=StoreType.LOCAL_ARTIFACT,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
def nasdaqapi(skip_download: bool, exchange: Optional[Exchange], store_type: StoreType):
    pipeline = NASDAQSymbolsPipeline(skip_download, exchange, store_type)
    pipeline.run()
