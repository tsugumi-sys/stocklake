import os
import tempfile

from stocklake.entities.file_info import FileInfo
from stocklake.utils.file_utils import (
    get_file_info,
    list_all,
)


def test_list_all():
    with tempfile.TemporaryDirectory() as tempdirname:
        example_filenames = ["example1.txt", "example2.txt"]
        example_filepaths = []
        for filename in example_filenames:
            filepath = os.path.join(tempdirname, filename)
            example_filepaths.append(filepath)
            with open(os.path.join(tempdirname, filename), "w") as f:
                f.write("test")

        assert sorted(list_all(tempdirname, full_path=False)) == example_filenames
        assert sorted(list_all(tempdirname, full_path=True)) == example_filepaths


def test_get_file_info():
    with tempfile.TemporaryDirectory() as tempdirname:
        assert get_file_info(tempdirname, tempdirname) == FileInfo(
            tempdirname, True, None
        )
        example_filepath = os.path.join(tempdirname, "example.txt")
        with open(example_filepath, "w") as f:
            f.write("test")
        assert get_file_info(example_filepath, example_filepath) == FileInfo(
            example_filepath, False, os.path.getsize(example_filepath)
        )
