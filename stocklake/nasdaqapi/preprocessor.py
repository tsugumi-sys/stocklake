import json
import os
import tempfile

import pandas as pd

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.stores.artifact.base import ArtifactRepository


class NASDAQSymbolsPreprocessor(BasePreprocessor):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        source_artifact_path_json: str,
        artifact_filename_csv: str = "data.csv",
    ):
        super().__init__(artifact_repo)
        self.source_artifact_path_json = source_artifact_path_json
        self.artifact_filename_csv = artifact_filename_csv

    @property
    def artifact_path(self):
        return os.path.join(self.artifact_repo.artifact_dir, self.artifact_filename_csv)

    def process(self):
        with open(self.source_artifact_path_json) as f:
            data = json.load(f)

        symbols_data = {k: [v] for k, v in data[0].items()}
        for d in data[1:]:
            for key, value in d.items():
                symbols_data[key].append(value)

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self.artifact_filename_csv)
            pd.DataFrame.from_dict(symbols_data).to_csv(
                os.path.join(tempdirname, self.artifact_filename_csv)
            )
            self.artifact_repo.log_artifact(local_file)


class NYSESymbolsPreprocessor(BasePreprocessor):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        source_artifact_path_json: str,
        artifact_filename_csv: str = "data.csv",
    ):
        super().__init__(artifact_repo)
        self.source_artifact_path_json = source_artifact_path_json
        self.artifact_filename_csv = artifact_filename_csv

    @property
    def artifact_path(self):
        return os.path.join(self.artifact_repo.artifact_dir, self.artifact_filename_csv)

    def process(self):
        with open(self.source_artifact_path_json) as f:
            data = json.load(f)

        symbols_data = {k: [v] for k, v in data[0].items()}
        for d in data[1:]:
            for key, value in d.items():
                symbols_data[key].append(value)

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self.artifact_filename_csv)
            pd.DataFrame.from_dict(symbols_data).to_csv(
                os.path.join(tempdirname, self.artifact_filename_csv)
            )
            self.artifact_repo.log_artifact(local_file)


class AMEXSymbolsPreprocessor(BasePreprocessor):
    def __init__(
        self,
        artifact_repo: ArtifactRepository,
        source_artifact_path_json: str,
        artifact_filename_csv: str = "data.csv",
    ):
        super().__init__(artifact_repo)
        self.source_artifact_path_json = source_artifact_path_json
        self.artifact_filename_csv = artifact_filename_csv

    @property
    def artifact_path(self):
        return os.path.join(self.artifact_repo.artifact_dir, self.artifact_filename_csv)

    def process(self):
        with open(self.source_artifact_path_json) as f:
            data = json.load(f)

        symbols_data = {k: [v] for k, v in data[0].items()}
        for d in data[1:]:
            for key, value in d.items():
                symbols_data[key].append(value)

        with tempfile.TemporaryDirectory() as tempdirname:
            local_file = os.path.join(tempdirname, self.artifact_filename_csv)
            pd.DataFrame.from_dict(symbols_data).to_csv(
                os.path.join(tempdirname, self.artifact_filename_csv)
            )
            self.artifact_repo.log_artifact(local_file)
