import os

import pytest

from stocklake.stores.constants import StoreType
from stocklake.wiki_sp500.data_loader import WikiSP500DataLoader
from stocklake.wiki_sp500.preprocessor import WikiSP500Preprocessor
from stocklake.wiki_sp500.stores import WikiSP500Stores


@pytest.fixture
def wiki_sp500_data():
    data_loader = WikiSP500DataLoader()
    preprocessor = WikiSP500Preprocessor()
    yield preprocessor.process(data_loader.download())


def test_save_local_artifact_repo(wiki_sp500_data):
    store = WikiSP500Stores()
    saved_path = store.save(StoreType.LOCAL_ARTIFACT, wiki_sp500_data)
    assert os.path.exists(saved_path)
