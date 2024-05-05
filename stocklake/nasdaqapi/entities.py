from typing import List, TypedDict


class RawNasdaqApiSymbolData(TypedDict):
    symbol: str
    name: str
    lastsale: str
    netchange: str
    pctchange: str
    volume: str
    marketCap: str
    country: str
    ipoyear: str
    industry: str
    sector: str
    url: str


class NasdaqApiSymbolData(TypedDict):
    symbol: str
    name: str
    last_sale: float
    net_change: float
    pct_change: float
    marketcap: float
    volume: float
    country: str
    ipo_year: int
    industry: str
    sector: str
    url: str


class _ResponseData(TypedDict):
    asOf: str
    headers: RawNasdaqApiSymbolData
    rows: List[RawNasdaqApiSymbolData]


class NasdaqAPIResponse(TypedDict):
    data: _ResponseData
