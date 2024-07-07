from stocklake.wiki_sp500.data_loader import WikiSP500DataLoader
from stocklake.wiki_sp500.preprocessor import WikiSP500Preprocessor


def test_process():
    data_loader = WikiSP500DataLoader()
    preprocessor = WikiSP500Preprocessor()
    for r in preprocessor.process(data_loader.download()):
        assert isinstance(r.symbol, str)
        assert isinstance(r.company, str)
        assert isinstance(r.sector, (str, None))
        assert isinstance(r.industry, (str, None))
        assert isinstance(r.headquarters, (str, None))
