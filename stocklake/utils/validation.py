import posixpath

from stocklake.exceptions import StockLakeException
from stocklake.stores.constants import StoreType


def path_not_unique(name: str):
    norm = posixpath.normpath(name)
    return norm != name or norm == "." or norm.startswith("..") or norm.startswith("/")


def validate_store_type(store_type: str | None):
    if store_type not in StoreType.types():
        raise StockLakeException(
            f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
        )
