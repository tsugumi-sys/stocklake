from typing import List, Optional, TypedDict

from pydantic import BaseModel, ConfigDict


class TD_RawNasdaqApiData(TypedDict):
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


class RawNasdaqApiData(BaseModel):
    model_config = ConfigDict(extra="forbid")
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


class NasdaqApiDataBase(BaseModel):
    symbol: str
    exchange: str
    name: str
    last_sale: float
    net_change: float
    pct_change: Optional[float]
    marketcap: float
    volume: float
    country: str
    ipo_year: int
    industry: str
    sector: str
    url: str


class PreprocessedNasdaqApiData(NasdaqApiDataBase):
    pass


class NasdaqApiDataCreate(NasdaqApiDataBase):
    pass


class NasdaqApiData(NasdaqApiDataBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: int
    updated_at: int


class _ResponseData(TypedDict):
    asOf: str
    headers: TD_RawNasdaqApiData
    rows: List[TD_RawNasdaqApiData]


class NasdaqAPIResponse(TypedDict):
    data: _ResponseData
