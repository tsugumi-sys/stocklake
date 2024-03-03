from sqlalchemy import create_engine, orm

from stocklake.environment_variables import (
    STOCKLAKE_POSTGRES_DATABASE,
    STOCKLAKE_POSTGRES_HOST,
    STOCKLAKE_POSTGRES_PASSWORD,
    STOCKLAKE_POSTGRES_USER,
)

Base = orm.declarative_base()

LocalEngine = create_engine(
    f"postgresql://{STOCKLAKE_POSTGRES_USER.get()}:{STOCKLAKE_POSTGRES_PASSWORD.get()}@{STOCKLAKE_POSTGRES_HOST.get()}/{STOCKLAKE_POSTGRES_DATABASE.get()}",
)

LocalSession = orm.sessionmaker(autocommit=False, bind=LocalEngine)
