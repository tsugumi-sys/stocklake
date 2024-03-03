import pytest
from sqlalchemy import create_engine, orm
from sqlalchemy_utils import create_database, database_exists, drop_database

from stocklake.environment_variables import (
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)
from stocklake.exceptions import StockLoaderException
from stocklake.stores.db.models import Base


@pytest.fixture(scope="function")
def SessionLocal():
    TEST_SQLALCHEMY_URL = f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/test"
    engine = create_engine(TEST_SQLALCHEMY_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise StockLoaderException("Test database already exists")

    # Create test database
    Base.metadata.create_all(engine)
    SessionLocal = orm.sessionmaker(autocommit=False, bind=engine)
    yield SessionLocal

    # Drop the test database after finishing test
    drop_database(TEST_SQLALCHEMY_URL)
