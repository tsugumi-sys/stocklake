import pytest
from sqlalchemy import create_engine, orm
from sqlalchemy_utils import create_database, database_exists, drop_database

from stocklake.exceptions import StockLakeException
from stocklake.stores.db.database import database_url
from stocklake.stores.db.models import Base


@pytest.fixture(scope="function", autouse=True)
def set_environment_variables(monkeypatch):
    monkeypatch.setenv("STOCKLAKE_POLYGON_API_KEY", "dummy_key")
    monkeypatch.setenv("_STOCKLAKE_ENVIRONMENT", "test")


@pytest.fixture(scope="function")
def SessionLocal(monkeypatch):
    engine = create_engine(database_url())

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise StockLakeException("Test database already exists")

    # Create tables
    Base.metadata.create_all(engine)
    SessionLocal = orm.sessionmaker(autocommit=False, bind=engine)
    yield SessionLocal

    # Drop the test database after finishing tests
    drop_database(database_url())


@pytest.fixture(scope="function")
def test_database(monkeypatch):
    engine = create_engine(database_url())

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise StockLakeException("Test database already exists")

    yield

    # Drop the test database after finishing tests
    drop_database(database_url())
