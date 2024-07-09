from stocklake.environment_variables import STOCKLAKE_POLYGON_API_KEY
from stocklake.exceptions import StockLakeException


def validate_polygonapi_api_key():
    if STOCKLAKE_POLYGON_API_KEY.get() is None:
        raise StockLakeException(
            "You need to set an environment variable `STOCKLAKE_POLYGON_API_KEY`."
        )
