import click

from stocklake.nasdaqapi.cli import nasdaqapi
from stocklake.stores.db.cli import upgrade


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
database.add_command(upgrade)

cli.add_command(download)
cli.add_command(database)
