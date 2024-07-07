import logging
from typing import Optional

from stocklake.core.base_pipeline import BasePipeline
from stocklake.core.stdout import PipelineStdOut
from stocklake.stores.constants import StoreType
from stocklake.stores.db.database import DATABASE_SESSION_TYPE, local_session
from stocklake.utils.validation import validate_store_type
from stocklake.wiki_sp500.data_loader import WikiSP500DataLoader
from stocklake.wiki_sp500.preprocessor import WikiSP500Preprocessor
from stocklake.wiki_sp500.stores import WikiSP500Store

logger = logging.getLogger(__name__)


class WikiSP500Pipeline(BasePipeline):
    def __init__(
        self,
        skip_download: bool = False,
        store_type: StoreType = StoreType.LOCAL_ARTIFACT,
        sqlalchemy_session: Optional[DATABASE_SESSION_TYPE] = None,
    ):
        self.skip_download = skip_download

        validate_store_type(store_type)
        self.store_type = store_type
        if sqlalchemy_session is None:
            sqlalchemy_session = local_session()

        self.data_loader = (
            WikiSP500DataLoader(use_cache=True)
            if self.skip_download
            else WikiSP500DataLoader()
        )
        self.preprocessor = WikiSP500Preprocessor()
        self.store = WikiSP500Store(sqlalchemy_session)
        self.stdout = PipelineStdOut()

    def run(self):
        self.stdout.starting("Wikipedia S&P500")
        if self.skip_download:
            self.stdout.skip_downloading()
        else:
            self.stdout.downloading()
        raw_data = self.data_loader.download()
        data = self.preprocessor.process(raw_data)
        saved_location = self.store.save(self.store_type, data)
        self.stdout.completed(saved_location)
