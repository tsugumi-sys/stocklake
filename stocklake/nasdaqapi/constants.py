from enum import Enum


class Exchange(str, Enum):
    NASDAQ = "nasdaq"
    NYSE = "nyse"
    AMEX = "amex"

    @classmethod
    def exchanges(self):
        return sorted([e for e in Exchange.__members__])
