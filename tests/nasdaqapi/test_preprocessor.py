import json

from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.preprocessor import NASDAQSymbolsPreprocessor

with open("./tests/nasdaqapi/sample_response.json") as f:
    mock_raw_data = json.load(f)["data"]["rows"]


def test_process():
    preprocessor = NASDAQSymbolsPreprocessor()
    data = preprocessor.process(exchange=Exchange.NASDAQ, data=mock_raw_data)
    for data_dic in data:
        for key, val in data_dic.items():
            if key in ["last_sale", "net_change", "pct_change", "marketcap", "volume"]:
                assert isinstance(val, float)
            elif key in ["ipo_year"]:
                assert isinstance(val, int)
            else:
                assert isinstance(val, str)
