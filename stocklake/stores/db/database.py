from sqlalchemy import create_engine, orm

from stocklake.environment_variables import (
    _STOCKLAKE_ENVIRONMENT,
    STOCKLAKE_POSTGRES_DATABASE,
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)

Base = orm.declarative_base()


def database_url():
    """Dynamically change database url based on environment variable `__STOCKLAKE_ENVIRONMENT`"""
    DATABASE_NAME = (
        STOCKLAKE_POSTGRES_DATABASE.get()
        if _STOCKLAKE_ENVIRONMENT.get() == "production"
        else "test"
    )
    return f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/{DATABASE_NAME}"


def local_session() -> orm.sessionmaker[orm.session.Session]:
    LocalEngine = create_engine(database_url())
    return orm.sessionmaker(autocommit=False, bind=LocalEngine)
