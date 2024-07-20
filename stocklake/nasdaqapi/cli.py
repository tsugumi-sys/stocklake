from typing import Optional

import click

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.pipeline import NASDAQSymbolsPipeline
from stocklake.stores.constants import ArtifactFormat, StoreType


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
    default=None,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
@click.option(
    "--artifact_format",
    default=None,
    help=f"The artifact file format, should be in `{ArtifactFormat.formats()}`",
)
def nasdaqapi(
    skip_download: bool,
    exchange: Optional[Exchange],
    store_type: StoreType | None,
    artifact_format: ArtifactFormat | None,
):
    pipeline = NASDAQSymbolsPipeline(
        skip_download, exchange, store_type, artifact_format
    )
    pipeline.run()
