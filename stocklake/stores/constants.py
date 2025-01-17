from enum import Enum


class StoreType(str, Enum):
    LOCAL_ARTIFACT = "local_artifact"
    POSTGRESQL = "postgresql"

    @staticmethod
    def types():
        return sorted([t.value for t in StoreType])

    def __str__(self):
        return self.value


class ArtifactFormat(str, Enum):
    CSV = "csv"
    JSON = "json"

    @staticmethod
    def formats():
        return sorted(t.value for t in ArtifactFormat)

    def __str__(self):
        return self.value
