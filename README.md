# stocklake

[![PyPI - Version](https://img.shields.io/pypi/v/stocklake.svg)](https://pypi.org/project/stocklake)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stocklake.svg)](https://pypi.org/project/stocklake)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install stocklake
```

## Quick start

pre requesties:
- docker && docker compose

### 1. setup docker compose

Let's create docker compose file.

```sh
touch docker-compose.yml
```

Copy [this docker compose file](https://github.com/tsugumi-sys/stocklake/blob/main/docker-compose.yml) contents into the your docker compose file.

Then, run docker containers.

```sh
docker compose up -d
```

This command builds the following 3 containers.

- PostgreSQL for stocklake data.
- [Metabase Web UI](http://localhost:3000)
- PostgreSQL for metabase.

### 2. Download NASDAQ API data.

Run the following command to download data from [nasdaq API](https://www.nasdaq.com/) and save into PostgreSQL.

```
stocklake download nasdaqapi --exchange nasdaq --store_type postgresql
```

### 3. Setup metabase

Accessing the metabase web ui ([Metabase Web UI](http://localhost:3000)) and setup connection of stocklake PostgreSQL database with the following settings.

| section | value |
| :---- | :---- |
| Database Type | `PostgreSQL` |
| Host | `stocklake-db` |
| Port | `5432` |
| Database name | `stocklake` |
| Username | `postgres` |
| Password | `password` |

Other settings can be theier default values.

Now you can see the Nasdaq API data on your metabase dashborad!

## Supported APIs

| name | status | API Docs | Additional Information |
| :--- | :---: | :--- | :--- |
| Nasdaq API (Screener) | :white_check_mark: | [URL](https://www.nasdaq.com/market-activity/stocks/screener) | |
| Polygon API (Stock Financials Vx) | :white_check_mark: | [URL](https://polygon.io/docs/stocks/get_vx_reference_financials) | [Data Fields Information](https://polygon.io/blog/financials-api-glossary-of-fields) |
| Polygon API (Tickers) | :construction: | [URL](https://polygon.io/docs/stocks/get_v3_reference_tickers) | |

## Examples

### Nasdaq API (Screener)

```bash
stocklake download nasdaqapi --exchange nasdaq --store_type postgresql
```

### Polygon API (Stock Financials Vx)

```bash
stocklake download polygonapi --symbols AAPL --api_type stock_financials_vx --store_type postgresql
```


## License

`stocklake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
