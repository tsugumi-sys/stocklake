from abc import ABC, abstractmethod

from stocklake.stores.artifact.base import ArtifactRepository


class BasePreprocessor(ABC):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
    ):
        self._artifact_repo = artifact_repo

    @property
    def artifact_repo(self) -> ArtifactRepository:
        return self._artifact_repo

    @abstractmethod
    def process(self, *args, **kwargs):
        pass
