import click

from stocklake.nasdaqapi.cli import nasdaqapi
from stocklake.polygonapi.cli import polygonapi
from stocklake.stores.db.cli import autogenerate_revision, upgrade
from stocklake.wiki_sp500.cli import wikisp500


@click.group()
def stocklake():
    pass


@click.group()
def download():
    """
    Download data to several stores from APIs.

    e.g.

    The following command downloads table data of Nasdaq API data into local csv file.

    ```bash
    stocklake download nasdaqapi --exchange nasdaq
    ```
    """
    pass


@click.group()
def database():
    """Manage database schemas."""
    pass


download.add_command(nasdaqapi)
download.add_command(polygonapi)
download.add_command(wikisp500)

database.add_command(upgrade)
database.add_command(autogenerate_revision)

stocklake.add_command(download)
stocklake.add_command(database)
