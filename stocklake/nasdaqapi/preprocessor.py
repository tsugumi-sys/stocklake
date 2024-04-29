from typing import List

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.nasdaqapi.entities import NasdaqApiSymbolData, RawNasdaqApiSymbolData


class NASDAQSymbolsPreprocessor(BasePreprocessor):
    def process(self, data: List[RawNasdaqApiSymbolData]) -> List[NasdaqApiSymbolData]:
        processed_data: List[NasdaqApiSymbolData] = []
        for data_dic in data:
            _data: NasdaqApiSymbolData = {
                "symbol": data_dic["symbol"],
                "name": data_dic["name"],
                "lastsale": float(
                    data_dic["lastsale"].replace("$", "").replace(",", "")
                ),
                "netchange": float(data_dic["netchange"]),
                "pctchange": float(data_dic["pctchange"].replace("%", "")),
                "marketCap": float(data_dic["marketCap"].replace(",", "")),
                "url": data_dic["url"],
            }
            processed_data.append(_data)
        return processed_data
