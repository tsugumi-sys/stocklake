from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from stocklake.stores.db.database import Base


class NasdaqApiData(Base):
    __tablename__ = "nasdaq_api_data"

    id = Column(Integer, primary_key=True)
    exchange = Column(String(10))
    symbol = Column(String(10))
    name = Column(String(256))
    last_sale = Column(Float)
    pct_change = Column(Float)
    net_change = Column(Float)
    volume = Column(Float)
    marketcap = Column(Float)
    country = Column(String)
    ipo_year = Column(Integer)
    industry = Column(String)
    sector = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
