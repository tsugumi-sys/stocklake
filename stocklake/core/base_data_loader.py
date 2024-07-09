from abc import ABC, abstractmethod
from typing import List


class BaseDataLoader(ABC):
    @property
    @abstractmethod
    def cache_artifact_path(self) -> str:
        pass

    @property
    @abstractmethod
    def cache_artifact_paths(self) -> List[str]:
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass
