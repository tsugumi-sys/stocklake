from abc import ABC, abstractmethod


class BaseDataLoader(ABC):
    @property
    @abstractmethod
    def cache_artifact_path(self) -> str:
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass
