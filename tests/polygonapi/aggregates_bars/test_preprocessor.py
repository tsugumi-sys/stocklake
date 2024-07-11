from stocklake.polygonapi.aggregates_bars.data_loader import (
    PolygonAggregatesBarsDataLoader,
)
from stocklake.polygonapi.aggregates_bars.preprocessor import (
    PolygonAggregatesBarsPreprocessor,
)
from tests.polygonapi.aggregates_bars.test_data_loader import (
    MockPolygonAggregatesBarsAPIServer,  # noqa: F401
)


def test_preprocess(MockPolygonAggregatesBarsAPIServer):  # noqa: F811
    data_loader = PolygonAggregatesBarsDataLoader()
    preprocessor = PolygonAggregatesBarsPreprocessor()
    preprocessed_data = preprocessor.process(data_loader.download(["AAPL"]))
    for d in preprocessed_data:
        assert d.ticker == "AAPL"
        for item in [d.open, d.high, d.low, d.close, d.volume_weighted_average_price]:
            assert isinstance(item, float)
        for item in [d.timestamp_ms, d.transactions, d.volume]:
            assert isinstance(item, int)
