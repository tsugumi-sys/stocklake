from typing import Optional

import click

from stocklake.exceptions import StockLoaderException
from stocklake.polygonapi.constants import PolygonAPIType
from stocklake.polygonapi.pipeline import PolygonFinancialsDataPipeline
from stocklake.stores.constants import StoreType


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
)
@click.option("--symbols", default=None, help="symbols split by comma. ex `MSFT,AAPL`.")
@click.option(
    "--api_type",
    default=None,
    help=f"Polygon API Type, supported type is {PolygonAPIType.types()}. See docs for more information; https://polygon.io/docs/stocks/getting-started",
)
@click.option(
    "--store_type",
    default=StoreType.LOCAL_ARTIFACT,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
def polygonapi(
    skip_download: bool,
    symbols: Optional[str],
    api_type: Optional[str],
    store_type: StoreType,
):
    if symbols is None:
        raise StockLoaderException("`symbols` must be given.")

    if api_type is None:
        raise StockLoaderException(
            f"`api_type` must be given, supported type is {PolygonAPIType.types()}"
        )
    if api_type not in PolygonAPIType.types():
        raise StockLoaderException(
            f"Invalid `api_type` {api_type}, supported type is {PolygonAPIType.types()}"
        )

    if api_type == PolygonAPIType.STOCK_FINANCIALS_VX:
        pipeline = PolygonFinancialsDataPipeline(
            symbols.split(","), skip_download, store_type
        )
    else:
        raise NotImplementedError
    pipeline.run()
