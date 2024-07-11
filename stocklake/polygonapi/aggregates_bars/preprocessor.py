import logging
from typing import Dict, List

from polygon.rest.models.aggs import Agg

from stocklake.core.base_preprocessor import BasePreprocessor
from stocklake.polygonapi.aggregates_bars.entities import (
    PreprocessedPolygonAggregatesBarsData,
)

logger = logging.getLogger(__name__)


class PolygonAggregatesBarsPreprocessor(BasePreprocessor):
    def process(
        self, data: Dict[str, List[Agg]]
    ) -> List[PreprocessedPolygonAggregatesBarsData]:
        preprocessed_data = []
        for ticker, ohlc in data.items():
            for row in ohlc:
                preprocessed_data.append(
                    PreprocessedPolygonAggregatesBarsData(
                        ticker=ticker,
                        timestamp_ms=row.timestamp,
                        open=row.open,
                        high=row.high,
                        low=row.low,
                        close=row.close,
                        transactions=row.transactions,
                        volume=row.volume,
                        volume_weighted_average_price=row.vwap,
                    )
                )
        return preprocessed_data
