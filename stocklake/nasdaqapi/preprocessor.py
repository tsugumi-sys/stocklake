from typing import List

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.nasdaqapi.entities import RawNasdaqApiSymbolData


class NASDAQSymbolsPreprocessor(BasePreprocessor):
    def process(
        self, data: List[RawNasdaqApiSymbolData]
    ) -> List[RawNasdaqApiSymbolData]:
        return data
