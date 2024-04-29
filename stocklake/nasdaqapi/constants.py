from enum import Enum


class Exchange(str, Enum):
    NASDAQ = "nasdaq"
    NYSE = "nyse"
    AMEX = "amex"

    @classmethod
    def exchanges(self):
        return sorted([e.value for e in Exchange])

    def __str__(self):
        return self.value
