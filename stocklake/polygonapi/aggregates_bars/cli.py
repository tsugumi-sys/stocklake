from typing import Optional

import click

from stocklake.exceptions import StockLakeException
from stocklake.polygonapi.aggregates_bars.pipeline import (
    PolygonAggregatesBarsDataPipeline,
)
from stocklake.stores.constants import ArtifactFormat, StoreType


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
@click.option(
    "--artifact_format",
    default=None,
    help=f"The artifact file format, should be in `{ArtifactFormat.formats()}`",
)
@click.option(
    "--interval_sec",
    default=0,
    help="The interval time in seconds to process each symbols",
)
def aggregates_bars(
    skip_download: bool,
    symbols: Optional[str],
    store_type: StoreType | None,
    artifact_format: ArtifactFormat | None,
    interval_sec: int,
):
    if symbols is None:
        raise StockLakeException("`symbols` must be given.")

    pipeline = PolygonAggregatesBarsDataPipeline(
        symbols.split(","), skip_download, store_type, artifact_format, interval_sec
    )
    pipeline.run()
