import os

import pytest

from stocklake.exceptions import StockLakeException
from stocklake.stores.constants import StoreType
from stocklake.stores.db.models import WikiSP500Data
from stocklake.wiki_sp500.pipeline import WikiSP500Pipeline
from stocklake.wiki_sp500.stores import SAVE_ARTIFACTS_DIR


def test_invalid_store_type_specified():
    with pytest.raises(StockLakeException) as exc:
        _ = WikiSP500Pipeline(store_type="INVALID_STORE_TYPE")
        assert "Specified store type is invalid, INVALID_STORE_TYPE" in str(exc.value)


def test_run_with_local_artifact():
    pipeline = WikiSP500Pipeline(store_type=StoreType.LOCAL_ARTIFACT)
    pipeline.run()
    assert os.path.exists(os.path.join(SAVE_ARTIFACTS_DIR, "wiki_sp500.csv"))


def test_run_with_postresql(SessionLocal):
    with SessionLocal() as session, session.begin():
        res = session.query(WikiSP500Data).all()
        assert len(res) == 0

    pipeline = WikiSP500Pipeline(store_type=StoreType.POSTGRESQL)
    pipeline.run()
    with SessionLocal() as session, session.begin():
        res = session.query(WikiSP500Data).all()
        assert len(res) > 0
