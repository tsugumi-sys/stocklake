from typing import List

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import PreprocessedNasdaqApiData, RawNasdaqApiData


class NASDAQSymbolsPreprocessor(BasePreprocessor):
    def process(
        self, exchange: Exchange, data: List[RawNasdaqApiData]
    ) -> List[PreprocessedNasdaqApiData]:
        processed_data = []
        for d in data:
            _data = {
                "symbol": d.symbol,
                "exchange": exchange,
                "name": d.name,
                "last_sale": float(d.lastsale.replace("$", "").replace(",", "")),
                "pct_change": (
                    None if d.pctchange == "" else float(d.pctchange.replace("%", ""))
                ),
                "net_change": float(d.netchange),
                "volume": float(d.volume),
                "marketcap": self._market_cap(d),
                "country": d.country,
                "ipo_year": self._ipo_year(d),
                "industry": d.industry,
                "sector": d.sector,
                "url": d.url,
            }
            # NOTE: We ignore arg-type mypy error here, because of this bug https://github.com/python/mypy/issues/5382.
            processed_data.append(PreprocessedNasdaqApiData(**_data))  # type: ignore
        return processed_data

    def _ipo_year(self, data: RawNasdaqApiData) -> int:
        ipo_year = data.ipoyear
        if ipo_year == "":
            return 0
        return int(ipo_year)

    def _market_cap(self, data: RawNasdaqApiData) -> float:
        market_cap = data.marketCap.replace(",", "")
        if market_cap == "":
            return 0.0
        return float(market_cap)
