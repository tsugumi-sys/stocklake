import copy

from stocklake.nasdaqapi.sqlalchemy_store import NasdaqApiSQLAlchemyStore
from stocklake.stores.db.models import NasdaqApiData
from stocklake.stores.db.schemas import NasdaqStockCreate
from tests.stores.db.utils import SessionLocal  # noqa: F401


def test_NasdaqAPISQLAlchemyStore_create(SessionLocal):  # noqa: F811
    store = NasdaqApiSQLAlchemyStore(SessionLocal)
    data = {
        "symbol": "TEST",
        "last_sale": 0.88,
        "pct_change": 0.5,
        "net_change": 0.35,
        "volume": 100.5,
        "marketcap": 0.75,
        "country": "US",
        "ipo_year": 1999,
        "industry": "Tech",
        "sector": "Health",
        "url": "https://example.com",
    }

    # Add item
    store.create(NasdaqStockCreate(**data))
    with SessionLocal() as session, session.begin():
        res = session.query(NasdaqApiData).all()
        assert len(res) == 1

        stored_data = res[0]
        assert stored_data.symbol == data["symbol"]
        assert stored_data.last_sale == data["last_sale"]
        assert stored_data.pct_change == data["pct_change"]
        assert stored_data.net_change == data["net_change"]
        assert stored_data.volume == data["volume"]
        assert stored_data.marketcap == data["marketcap"]
        assert stored_data.country == data["country"]
        assert stored_data.ipo_year == data["ipo_year"]
        assert stored_data.industry == data["industry"]
        assert stored_data.sector == data["sector"]
        assert stored_data.url == data["url"]
        assert stored_data.created_at is not None
        assert stored_data.updated_at is not None

    # Add list of items
    data2 = copy.deepcopy(data)
    data2["symbol"] = "TEST2"
    data3 = copy.deepcopy(data)
    data3["symbol"] = "TEST3"
    store.create([NasdaqStockCreate(**data2), NasdaqStockCreate(**data3)])
    with SessionLocal() as session, session.begin():
        assert len(session.query(NasdaqApiData).all()) == 3
