# https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
import logging
import os
import tempfile
from typing import List

import requests
from bs4 import BeautifulSoup

from stocklake.core.base_data_loader import BaseDataLoader
from stocklake.core.constants import CACHE_DIR
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository
from stocklake.wiki_sp500.entities import RawWikiSP500Data

logger = logging.getLogger(__name__)

CACHE_DIR_PATH = os.path.join(CACHE_DIR, "wiki_sp500")


class WikiSP500DataLoader(BaseDataLoader):
    def __init__(self, cache_dir: str = CACHE_DIR_PATH, use_cache: bool = False):
        self._use_cache = use_cache
        self._cache_artifact_repo = LocalArtifactRepository(cache_dir)
        self._cache_artifact_filename = "wiki_sp500.html"

    @property
    def cache_artifact_path(self) -> str:
        return os.path.join(
            self._cache_artifact_repo.artifact_dir, self._cache_artifact_filename
        )

    def download(self) -> List[RawWikiSP500Data]:
        logger.info(
            "Loading S&P500 symbols data from `https://en.wikipedia.org/wiki/List_of_S%26P_500_companies`"
        )
        content: str
        if self._use_cache:
            with open(self.cache_artifact_path) as f:
                content = f.read()
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            }
            res = requests.get(
                "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                headers=headers,
            )
            self._save_content_to_cache(res.content.decode("utf-8"))
            content = res.content

        wiki_soup = BeautifulSoup(content, "html.parser")
        symbol_table = wiki_soup.find(attrs={"class": "wikitable sortable"})
        symbol_data_list = []

        for symbol in symbol_table.find_all("tr"):
            symbol_data_content = {}
            for td_count, symbol_data in enumerate(symbol.find_all("td")):
                if td_count == 0:
                    symbol_data_content["symbol"] = self._replace_new_line_code(
                        symbol_data.text.replace("\n", "")
                    )
                if td_count == 1:
                    symbol_data_content["company"] = self._replace_new_line_code(
                        symbol_data.text.replace("\n", "")
                    )
                if td_count == 3:
                    symbol_data_content["sector"] = self._replace_new_line_code(
                        symbol_data.text.replace("\n", "")
                    )
                if td_count == 4:
                    symbol_data_content["industry"] = self._replace_new_line_code(
                        symbol_data.text.replace("\n", "")
                    )
                if td_count == 5:
                    symbol_data_content["headquarters"] = self._replace_new_line_code(
                        symbol_data.text.replace("\n", "")
                    )

            if not symbol_data_content:
                continue

            for field in ["sector", "industry", "headquarters"]:
                if field not in symbol_data_content:
                    symbol_data_content[field] = None  # type: ignore
            symbol_data_list.append(RawWikiSP500Data(**symbol_data_content))
        return symbol_data_list

    def _save_content_to_cache(self, content: str):
        with tempfile.TemporaryDirectory() as tempdir:
            tmp_file_path = os.path.join(tempdir, self._cache_artifact_filename)
            with open(tmp_file_path, "w") as f:
                f.write(content)
            self._cache_artifact_repo.save_artifact(
                tmp_file_path, self._cache_artifact_filename
            )

    def _replace_new_line_code(self, text: str) -> str:
        return text.replace("\n", "")
