from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from stocklake.stores.db.base_sql_model import Base


class NasdaqStock(Base):
    __tablename__ = "nasdaq_stocks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True)
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
