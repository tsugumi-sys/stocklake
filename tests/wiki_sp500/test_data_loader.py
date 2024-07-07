import os

import pytest

from stocklake.wiki_sp500.data_loader import WikiSP500DataLoader


@pytest.mark.parametrize("use_cache", [False, True])
def test_download(use_cache):
    data_loader = WikiSP500DataLoader(use_cache=use_cache)
    results = data_loader.download()
    for r in results:
        assert isinstance(r.symbol, str)
        assert isinstance(r.company, str)
        assert isinstance(r.sector, (str, None))
        assert isinstance(r.industry, (str, None))
        assert isinstance(r.headquarters, (str, None))

    assert os.path.exists(data_loader.cache_artifact_path)
