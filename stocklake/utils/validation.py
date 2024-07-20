import posixpath
from typing import Any

from stocklake.exceptions import StockLakeException
from stocklake.stores.constants import ArtifactFormat, StoreType


def path_not_unique(name: str):
    norm = posixpath.normpath(name)
    return norm != name or norm == "." or norm.startswith("..") or norm.startswith("/")


def validate_store_type(store_type: str | None):
    if store_type not in StoreType.types():
        raise StockLakeException(
            f"Specified store type is invalid, {store_type}, valid types are {StoreType.types()}"
        )


def validate_artifact_format(format: str | None):
    if format not in ArtifactFormat.formats():
        raise StockLakeException(
            f"Specified artifact format is invalid, {format}, valid types are {ArtifactFormat.formats()}"
        )


def validate_int_variable(var: Any, var_key: str):
    if not isinstance(var, int):
        raise ValueError(
            f"{var_key} must be integer, but got {var} (type: {type(var)})"
        )


def validate_numeric_range(
    var: int | float,
    var_key: str,
    min_: int | float | None = None,
    max_: int | float | None = None,
):
    if min_ is not None and var < min_:
        raise ValueError(f"{var_key} must be greater than {min_}.")
    if max_ is not None and var > max_:
        raise ValueError(f"{var_key} must be less than {max_}.")
