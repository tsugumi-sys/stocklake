import json

from stocklake.nasdaqapi.preprocessor import NASDAQSymbolsPreprocessor

with open("./tests/nasdaqapi/sample_response.json") as f:
    mock_raw_data = json.load(f)["data"]["rows"]


def test_process():
    preprocessor = NASDAQSymbolsPreprocessor()
    data = preprocessor.process(mock_raw_data)
    for data_dic in data:
        for key, val in data_dic.items():
            if key in ["lastsale", "netchange", "pctchange", "marketCap"]:
                assert isinstance(val, float)
            else:
                assert isinstance(val, str)
