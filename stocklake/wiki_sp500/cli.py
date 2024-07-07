import click

from stocklake.stores.constants import StoreType
from stocklake.wiki_sp500.pipeline import WikiSP500Pipeline


@click.command()
@click.option(
    "--skip_download", default=False, help="if true, downloading data will be skipped."
)
@click.option(
    "--store_type",
    default=StoreType.LOCAL_ARTIFACT,
    help=f"The storege type, should be in `{StoreType.types()}`.",
)
def wikisp500(skip_download: bool, store_type: StoreType):
    pipeline = WikiSP500Pipeline(skip_download, store_type)
    pipeline.run()
