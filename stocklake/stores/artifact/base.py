import logging
from abc import ABC, abstractmethod
from typing import Optional, List


from exceptions import AccountLoaderException
from utils.validation import path_not_unique

logger = logging.getLogger(__name__)


class ArtifactRepository(ABC):
    def __init__(self, artifact_uri: str):
        self.artifact_uri = artifact_uri

    @abstractmethod
    def log_artifact(self, local_file: str, artifact_path: Optional[str] = None):
        pass

    @abstractmethod
    def list_artifacts(self, path: str) -> List[str]:
        pass


def verify_artifact_path(artifact_path: str):
    if artifact_path and path_not_unique(artifact_path):
        raise AccountLoaderException(f"Invalid artifact path: {artifact_path}")
