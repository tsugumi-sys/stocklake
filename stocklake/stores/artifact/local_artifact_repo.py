import contextlib
import os
import shutil
from typing import Optional

from stocklake.stores.artifact.base import ArtifactRepository, verify_artifact_path
from stocklake.utils.file_utils import (
    get_file_info,
    list_all,
    relative_path_to_artifact_path,
)


class LocalArtifactRepository(ArtifactRepository):
    def __init__(self, artifact_uri: str):
        super().__init__(artifact_uri)
        self._artifact_dir = artifact_uri

    @property
    def artifact_dir(self):
        return self._artifact_dir

    def save_artifact(self, local_file: str, artifact_path: Optional[str] = None):
        if artifact_path:
            verify_artifact_path(artifact_path)
            artifact_path = os.path.normpath(artifact_path)

        artifact_dir = (
            os.path.join(self.artifact_dir, artifact_path)
            if artifact_path
            else self.artifact_dir
        )
        if not os.path.exists(artifact_dir):
            os.makedirs(artifact_dir)

        with contextlib.suppress(shutil.SameFileError):
            shutil.copy2(
                local_file, os.path.join(artifact_dir, os.path.basename(local_file))
            )

    def list_artifacts(self, path: Optional[str] = None):
        if path:
            path = os.path.normpath(path)
        list_dir = os.path.join(self.artifact_dir, path) if path else self.artifact_dir
        if os.path.isdir(list_dir):
            artifact_files = list_all(list_dir, full_path=True)
            infos = [
                get_file_info(
                    f,
                    relative_path_to_artifact_path(
                        os.path.relpath(f, self.artifact_dir)
                    ),
                )
                for f in artifact_files
            ]
            return sorted(infos, key=lambda f: f.path)
        else:
            return []
