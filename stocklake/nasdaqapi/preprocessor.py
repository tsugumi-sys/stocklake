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
                "last_sale": float(
                    data_dic["lastsale"].replace("$", "").replace(",", "")
                ),
                "pct_change": float(data_dic["pctchange"].replace("%", "")),
                "net_change": float(data_dic["netchange"]),
                "volume": float(data_dic["volume"]),
                "marketcap": float(data_dic["marketCap"].replace(",", "")),
                "country": data_dic["country"],
                "ipo_year": self._ipo_year(data_dic),
                "industry": data_dic["industry"],
                "sector": data_dic["sector"],
                "url": data_dic["url"],
            }
            processed_data.append(_data)
        return processed_data

    def _ipo_year(self, data_dic: RawNasdaqApiSymbolData) -> int:
        ipo_year = data_dic["ipoyear"]
        if ipo_year == "":
            return 0
        return int(ipo_year)
