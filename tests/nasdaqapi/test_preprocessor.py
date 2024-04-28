import json
import os

from stocklake.nasdaqapi.preprocessor import NASDAQSymbolsPreprocessor
from stocklake.stores.artifact.local_artifact_repo import LocalArtifactRepository

SAMPLE_RESPONSE_JSON = "./tests/nasdaqapi/sample_response.json"


# TODO: Custom downloader wrapper is needed.
def _download_data(dirpath: str, datafile: str = "data.json") -> str:
    file_path = os.path.join(dirpath, datafile)
    with open(SAMPLE_RESPONSE_JSON) as f:
        data = json.load(f)
    with open(file_path, "w") as f:
        json.dump(data["data"]["rows"], f)
    return file_path


def test_NASDAQSymbolsPreprocessor(tmpdir):
    datafile_path = _download_data(tmpdir)
    preprocessor = NASDAQSymbolsPreprocessor(
        LocalArtifactRepository(tmpdir), datafile_path
    )

    # check no artifact exists before run
    assert not os.path.exists(preprocessor.artifact_path)
    preprocessor.process()
    assert os.path.exists(preprocessor.artifact_path)
