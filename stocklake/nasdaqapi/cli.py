from typing import Optional

import click

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped"
)
@click.option(
    "--exchange",
    default=None,
    help=f"The exchange name that you want to download, should be in {Exchange.exchanges()}",
)
def nasdaqapi(skip_download: bool, exchange: Optional[str]):
    pipeline = NASDAQSymbolsPipeline(skip_download, exchange)
    pipeline.run()
