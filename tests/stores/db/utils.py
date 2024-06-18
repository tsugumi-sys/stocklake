import pytest
from sqlalchemy import create_engine, orm
from sqlalchemy_utils import create_database, database_exists, drop_database

from stocklake.exceptions import StockLoaderException
from stocklake.stores.db.database import database_url
from stocklake.stores.db.models import Base


@pytest.fixture(scope="function")
def SessionLocal(monkeypatch):
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    engine = create_engine(database_url())

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise StockLoaderException("Test database already exists")

    # Create tables
    Base.metadata.create_all(engine)
    SessionLocal = orm.sessionmaker(autocommit=False, bind=engine)
    yield SessionLocal

    # Drop the test database after finishing tests
    drop_database(database_url())


@pytest.fixture(scope="function")
def test_database(monkeypatch):
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")
    engine = create_engine(database_url())

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise StockLoaderException("Test database already exists")

    yield

    # Drop the test database after finishing tests
    drop_database(database_url())
