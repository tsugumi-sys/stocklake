from pydantic import BaseModel


class PolygonAggregatesBarsDataBase(BaseModel):
    ticker: str
    timestamp_ms: int
    open: float
    high: float
    low: float
    close: float
    transactions: int
    volume: float
    volume_weighted_average_price: float


class PreprocessedPolygonAggregatesBarsData(PolygonAggregatesBarsDataBase):
    pass


class PolygonAggregatesBarsDataCreate(PolygonAggregatesBarsDataBase):
    pass
