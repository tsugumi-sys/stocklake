from abc import ABC, abstractmethod

from stocklake.stores.artifact.base import ArtifactRepository


class DataLoader(ABC):
    def __init__(self, artifact_repo: ArtifactRepository):
        self._artifact_repo = artifact_repo

    @property
    def artifact_repo(self):
        return self._artifact_repo

    @abstractmethod
    def download(self, *args, **kwargs):
        pass
