from typing import Optional

import click

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.stock_financials_vx.pipeline import (
    PolygonFinancialsDataPipeline,
)
from stocklake.stores.constants import StoreType


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
)
@click.option("--symbols", default=None, help="symbols split by comma. ex `MSFT,AAPL`.")
@click.option(
    "--store_type",
    default=StoreType.LOCAL_ARTIFACT,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
def stock_financials_vx(
    skip_download: bool,
    symbols: Optional[str],
    store_type: StoreType,
):
    if symbols is None:
        raise StockLakeException("`symbols` must be given.")

    pipeline = PolygonFinancialsDataPipeline(
        symbols.split(","), skip_download, store_type
    )
    pipeline.run()
