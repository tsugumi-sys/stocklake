import csv
import logging
from typing import Any

import requests

from stocklake.exceptions import StockLoaderException
from stocklake.nasdaqapi.constants import Exchange
from stocklake.nasdaqapi.entities import NasdaqAPIResponse

logger = logging.getLogger(__name__)


def save_data_to_csv(data: Any, csv_path: str):
    # Extract column headers from the keys of the first dictionary
    fieldnames = data[0].keys() if data else []

    # Write the data to a CSV file
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each dictionary as a row in the CSV file
        for row in data:
            writer.writerow(row)


def symbols_api_endpoint(exchange_name: Exchange) -> str:
    return f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange_name}&download=true"


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
