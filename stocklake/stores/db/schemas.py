from pydantic import BaseModel


class NasdaqStockBase(BaseModel):
    symbol: str
    name: str
    last_sale: float
    pct_change: float
    net_change: float
    volume: float
    marketcap: float
    country: str
    ipo_year: int
    industry: str
    sector: str
    url: str


class NasdaqStockCreate(NasdaqStockBase):
    pass


class NasdaqStock(NasdaqStockBase):
    id: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True
