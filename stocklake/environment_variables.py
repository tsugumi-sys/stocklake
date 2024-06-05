import os
from typing import Any


class _EnvironmentVariable:
    """Represents an environment variable"""

    def __init__(self, name: str, default: Any):
        self.name = name
        self.default = default

    @property
    def defined(self):
        return self.name in os.environ

    @property
    def env_name(self) -> str:
        return self.name

    def get(self):
        if (val := os.getenv(self.name)) is not None:
            return val
        return self.default


STOCKLAKE_POSTGRES_HOST = _EnvironmentVariable("STOCKLAKE_POSTGRES_HOST", "localhost")
STOCKLAKE_POSTGRES_USER = _EnvironmentVariable("STOCKLAKE_POSTGRES_USER", "postgres")
STOCKLAKE_POSTGRES_PASSWORD = _EnvironmentVariable(
    "STOCKLAKE_POSTGRES_PASSWOR", "password"
)
STOCKLAKE_POSTGRES_DATABASE = _EnvironmentVariable(
    "STOCKLAKE_POSTGRES_DATABASE", "stocklake"
)
STOCKLAKE_POLYGON_API_KEY = _EnvironmentVariable("STOCKLAKE_POLYGON_API_KEY", None)


###
# Internal Environment Variable
###
_STOCKLAKE_ENVIRONMENT = _EnvironmentVariable(
    "_STOCKLAKE_ENVIRONMENT", "production"
)  # or test
