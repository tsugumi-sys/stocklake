import os
import re
from typing import List, Tuple


def mock_responses(mockdir: str) -> List[Tuple[str, str]]:
    mocks = []
    for dname, _, files in os.walk(mockdir):
        for fname in files:
            if fname.endswith(".json"):
                abspath = os.path.join(dname, fname)
                with open(abspath) as f:
                    urllpath = abspath.replace(mockdir, "").replace("\\", "/")
                    urllpath = re.sub(".json$", "", urllpath)
                    urllpath = re.sub("/index$", "", urllpath)
                    # Windows will be sad. We support dev on Windows.
                    if "?" in urllpath:
                        raise Exception(f"use & instead of ? in path ${urllpath}")
                    urllpath = urllpath.replace("&", "?", 1)
                    if ":" in urllpath:
                        raise Exception(f"use ; instead of : in path ${urllpath}")
                    urllpath = urllpath.replace(";", ":", 1)
                    # print(abspath, urllpath)
                    mocks.append((urllpath, f.read()))
    return mocks
