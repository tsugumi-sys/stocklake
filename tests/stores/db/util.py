from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from stocklake.environment_variables import (
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)

STOCKLAKE_TEST_POSTGRES_HOST = f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/test"


@pytest.fixture(scope="session", autouse=True)
def test_database() -> Generator:
    engine = create_engine(STOCKLAKE_TEST_POSTGRES_HOST)
    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    try:
        conn.execute("drop database test")
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    conn.execute("create database test")
    conn.close()

    yield

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute("commit")
    conn.execute("drop database test")
    conn.close()
