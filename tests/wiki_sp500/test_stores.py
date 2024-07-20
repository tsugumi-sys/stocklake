import os  # noqa: I001

import pytest

from stocklake.stores.db.database import (
    database_url,
)
from stocklake.stores.constants import ArtifactFormat, StoreType
from stocklake.stores.db import models
from stocklake.wiki_sp500 import entities
from stocklake.wiki_sp500.data_loader import WikiSP500DataLoader
from stocklake.wiki_sp500.preprocessor import WikiSP500Preprocessor
from stocklake.wiki_sp500.stores import WikiSP500DataSQLAlchemyStore, WikiSP500Store


@pytest.fixture
def wiki_sp500_data():
    data_loader = WikiSP500DataLoader()
    preprocessor = WikiSP500Preprocessor()
    yield preprocessor.process(data_loader.download())


@pytest.mark.parametrize(
    "artifact_format", [None, ArtifactFormat.CSV, "INVALID_FORMAT"]
)
def test_save_local_artifact_repo(artifact_format, wiki_sp500_data):
    store = WikiSP500Store()
    if artifact_format in ArtifactFormat.formats() or artifact_format is None:
        saved_path = store.save(
            StoreType.LOCAL_ARTIFACT, wiki_sp500_data, artifact_format
        )
        assert os.path.exists(saved_path)
    else:
        with pytest.raises(NotImplementedError):
            _ = store.save(StoreType.LOCAL_ARTIFACT, wiki_sp500_data, artifact_format)


def test_save_postgresql(wiki_sp500_data, SessionLocal):
    store = WikiSP500Store(SessionLocal)
    saved_path = store.save(StoreType.POSTGRESQL, wiki_sp500_data)
    assert saved_path == os.path.join(
        database_url(), models.WikiSP500Data.__tablename__
    )
    with SessionLocal() as session, session.begin():
        assert len(session.query(models.WikiSP500Data).all()) == len(wiki_sp500_data)


def test_WikiSP500DataSQLAlchemyStore_delete(wiki_sp500_data, SessionLocal):
    store = WikiSP500DataSQLAlchemyStore(SessionLocal)
    store.create(
        [entities.WikiSP500DataCreate(**d.model_dump()) for d in wiki_sp500_data]
    )
    with SessionLocal() as session, session.begin():
        assert len(session.query(models.WikiSP500Data).all()) == len(wiki_sp500_data)


def test_WikiSP500DataSQLAlchemyStore_create(wiki_sp500_data, SessionLocal):
    store = WikiSP500DataSQLAlchemyStore(SessionLocal)
    store.create(
        [entities.WikiSP500DataCreate(**d.model_dump()) for d in wiki_sp500_data]
    )
    with SessionLocal() as session, session.begin():
        assert len(session.query(models.WikiSP500Data).all()) == len(wiki_sp500_data)

    store.delete()
    with SessionLocal() as session, session.begin():
        assert len(session.query(models.WikiSP500Data).all()) == 0
