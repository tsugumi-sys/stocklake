from typing import Any, Optional


class FileInfo:
    def __init__(self, path: str, is_dir: bool, file_size: Optional[int]):
        self._path = path
        self._is_dir = is_dir
        self._bytes = file_size

    def __eq__(self, other: Any) -> bool:
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def path(self) -> str:
        return self._path

    @property
    def is_dir(self) -> bool:
        return self._is_dir

    @property
    def file_size(self) -> Optional[int]:
        return self._bytes

    def __repr__(self):
        return f"FileInfo(path={self.path}, is_dir={self.is_dir}, file_size={self.file_size} Bytes)"
