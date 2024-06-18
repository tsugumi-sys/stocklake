import click

from stocklake.nasdaqapi.cli import nasdaqapi
from stocklake.polygonapi.cli import polygonapi
from stocklake.stores.db.cli import autogenerate_revision, upgrade


@click.group()
def cli():
    pass


@click.group()
def download():
    pass


@click.group()
def database():
    pass


download.add_command(nasdaqapi)
download.add_command(polygonapi)
database.add_command(upgrade)
database.add_command(autogenerate_revision)

cli.add_command(download)
cli.add_command(database)
