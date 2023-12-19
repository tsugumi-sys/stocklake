import click

from stocklake.nasdaqapi.cli import nasdaqapi


@click.group()
def cli():
    pass


@click.group()
def download():
    pass


download.add_command(nasdaqapi)
cli.add_command(download)
