import click

from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.wiki_sp500.pipeline import WikiSP500Pipeline


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
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
def wikisp500(
    skip_download: bool,
    store_type: StoreType | None,
    artifact_format: ArtifactFormat | None,
):
    pipeline = WikiSP500Pipeline(skip_download, store_type, artifact_format)
    pipeline.run()
