import pytest

from stocklake.utils.validation import path_not_unique


@pytest.mark.parametrize(
    "name, expected", [("..", True), (".", True), ("/test/a", True), ("test/a", False)]
)
def test_path_not_unique(name, expected):
    assert path_not_unique(name) == expected
