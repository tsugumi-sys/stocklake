from typing import List, TypedDict


class RawNasdaqApiSymbolData(TypedDict):
    symbol: str
    name: str
    lastsale: str
    netchange: str
    pctchange: str
    marketCap: str
    url: str


class NasdaqApiSymbolData(TypedDict):
    symbol: str
    name: str
    lastsale: float
    netchange: float
    pctchange: float
    marketCap: float
    url: str


class _ResponseData(TypedDict):
    asOf: str
    headers: RawNasdaqApiSymbolData
    rows: List[RawNasdaqApiSymbolData]


class NasdaqAPIResponse(TypedDict):
    data: _ResponseData
