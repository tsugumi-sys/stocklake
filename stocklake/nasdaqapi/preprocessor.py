from typing import List

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqApiSymbolData, RawNasdaqApiSymbolData


class NASDAQSymbolsPreprocessor(BasePreprocessor):
    def process(
        self, exchange: Exchange, data: List[RawNasdaqApiSymbolData]
    ) -> List[NasdaqApiSymbolData]:
        processed_data: List[NasdaqApiSymbolData] = []
        for data_dic in data:
            _data: NasdaqApiSymbolData = {
                "symbol": data_dic["symbol"],
                "exchange": exchange,
                "name": data_dic["name"],
                "last_sale": float(
                    data_dic["lastsale"].replace("$", "").replace(",", "")
                ),
                "pct_change": (
                    None
                    if data_dic["pctchange"] == ""
                    else float(data_dic["pctchange"].replace("%", ""))
                ),
                "net_change": float(data_dic["netchange"]),
                "volume": float(data_dic["volume"]),
                "marketcap": self._market_cap(data_dic),
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

    def _market_cap(self, data_dic: RawNasdaqApiSymbolData) -> float:
        market_cap = data_dic["marketCap"].replace(",", "")
        if market_cap == "":
            return 0.0
        return float(market_cap)
