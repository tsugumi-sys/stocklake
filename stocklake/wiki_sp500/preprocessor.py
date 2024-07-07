from typing import List

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.wiki_sp500.entities import PreprocessedWikiSp500Data, RawWikiSP500Data


class WikiSP500Preprocessor(BasePreprocessor):
    def process(self, data: List[RawWikiSP500Data]) -> List[PreprocessedWikiSp500Data]:
        return [PreprocessedWikiSp500Data(**d.model_dump()) for d in data]
