from typing import Optional

import click

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars.pipeline import (
    PolygonAggregatesBarsDataPipeline,
)
from stocklake.stores.constants import StoreType


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
)
@click.option("--symbols", default=None, help="symbols split by comma. ex `MSFT,AAPL`.")
@click.option(
    "--store_type",
    default=None,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
def aggregates_bars(
    skip_download: bool,
    symbols: Optional[str],
    store_type: StoreType | None,
):
    if symbols is None:
        raise StockLakeException("`symbols` must be given.")

    pipeline = PolygonAggregatesBarsDataPipeline(
        symbols.split(","), skip_download, store_type
    )
    pipeline.run()
