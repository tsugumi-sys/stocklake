import click

from stocklake.polygonapi.stock_financials_vx.cli import stock_financials_vx


@click.group()
def polygonapi():
    pass


polygonapi.add_command(stock_financials_vx)
