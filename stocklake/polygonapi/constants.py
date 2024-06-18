from enum import StrEnum


class PolygonAPIType(StrEnum):
    STOCK_FINANCIALS_VX = "stock_financials_vx"

    @staticmethod
    def types():
        return sorted([t.value for t in PolygonAPIType])

    def __str__(self):
        return self.value
