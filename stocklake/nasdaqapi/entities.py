from typing import TypedDict


class NasdaqApiSymbolData(TypedDict):
    symbol: str
    name: str
    lastsale: str
    netchange: str
    pctchange: str
    marketCap: str
    url: str
