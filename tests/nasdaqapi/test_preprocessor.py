from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.data_loader import NASDAQSymbolsDataLoader
from stocklake.nasdaqapi.preprocessor import NASDAQSymbolsPreprocessor
from tests.nasdaqapi.test_data_loader import MockNasdaqAPIServer  # noqa: F401


def test_process(tmpdir, MockNasdaqAPIServer):  # noqa: F811
    data_loader = NASDAQSymbolsDataLoader(exchange_name=Exchange.AMEX, cache_dir=tmpdir)
    preprocessor = NASDAQSymbolsPreprocessor()
    data = preprocessor.process(exchange=Exchange.NASDAQ, data=data_loader.download())
    for data_dic in data:
        for key, val in data_dic.items():
            if key in ["last_sale", "net_change", "pct_change", "marketcap", "volume"]:
                assert isinstance(val, float)
            elif key in ["ipo_year"]:
                assert isinstance(val, int)
            else:
                assert isinstance(val, str)
