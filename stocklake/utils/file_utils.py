import os
import posixpath
from typing import List
from urllib.parse import unquote
from urllib.request import pathname2url

from stocklake.entities.file_info import FileInfo
from stocklake.exceptions import StockLoaderException


def list_all(
    root: str, filter_func=lambda x: True, full_path: bool = False
) -> List[str]:
    if not os.path.isdir(root):
        raise Exception(f"Invalid parent directory '{root}'")
    matches = [x for x in os.listdir(root) if filter_func(os.path.join(root, x))]
    return [os.path.join(root, m) for m in matches] if full_path else matches


def get_file_info(path: str, rel_path: str) -> FileInfo:
    if os.path.isdir(path):
        return FileInfo(path, True, None)
    else:
        return FileInfo(path, False, os.path.getsize(path))


def relative_path_to_artifact_path(path: str) -> str:
    if os.path == posixpath:
        return path
    if os.path.abspath(path) == path:
        raise StockLoaderException("This method only works with relative paths.")
    return unquote(pathname2url(path))
