import logging

import requests

from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqAPIResponse

logger = logging.getLogger(__name__)

BASE_URL = "https://api.nasdaq.com/api"


def symbols_api_endpoint(exchange_name: Exchange) -> str:
    return f"{BASE_URL}/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange_name}&download=true"


CUSTOM_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"
)
CUSTOM_HEADERS = {"user-agent": CUSTOM_USER_AGENT}


def nasdaq_api_get_request(exchange: Exchange) -> NasdaqAPIResponse:
    res = requests.get(symbols_api_endpoint(exchange), headers=CUSTOM_HEADERS)
    if res.status_code != 200:
        raise StockLoaderException(
            f"Request Failed with status code: {res.status_code}. All response body is the following: {res.text}"
        )

    response_body: NasdaqAPIResponse = res.json()
    return response_body
