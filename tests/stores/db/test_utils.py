from stocklake.stores.db.utils import create_sqlalchemy_engine

_environments = {
    "STOCKLAKE_POSTGRES_USER": "test-user",
    "STOCKLAKE_POSTGRES_HOST": "somehost",
    "STOCKLAKE_POSTGRES_PASSWORD": "testpassword",
    "STOCKLAKE_POSTGRES_DATABASE": "testdatabase",
}


def test_create_sqlalchemy_engine(monkeypatch):
    for key, val in _environments.items():
        monkeypatch.setenv(key, val)
    # Check successfully build engine
    engine = create_sqlalchemy_engine()
    assert str(engine.url) == "postgresql://{}:{}@{}/{}".format(
        _environments["STOCKLAKE_POSTGRES_USER"],
        "***",  # password is masked by sqlalchemy
        _environments["STOCKLAKE_POSTGRES_HOST"],
        _environments["STOCKLAKE_POSTGRES_DATABASE"],
    )
