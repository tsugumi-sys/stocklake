# stocklake

[![PyPI - Version](https://img.shields.io/pypi/v/stocklake.svg)](https://pypi.org/project/stocklake)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stocklake.svg)](https://pypi.org/project/stocklake)

A CLI tool to install stock information from various APIs to your data sources (local artifacts, databases, ...etc).

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install stocklake
```

## Supported APIs

| name | status | API Docs | Additional Information |
| :--- | :---: | :--- | :--- |
| Nasdaq API (Screener) | ✅ | [URL](https://www.nasdaq.com/market-activity/stocks/screener) | |
| Polygon API (Stock Financials Vx) | ✅ | [URL](https://polygon.io/docs/stocks/get_vx_reference_financials) | [Data Fields Information](https://polygon.io/blog/financials-api-glossary-of-fields) |
| Polygon API (Tickers) | ✅  | [URL](https://polygon.io/docs/stocks/get_v3_reference_tickers) | |
| Wikipedia: List of S&P 500 companies | ✅ | [URL](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) |  |

## Basic Usage

### Install Wikipedia: List of S&P 500 companies data to a local CSV file.

```bash
stocklake download wikisp500 --store_type local_artifact --artifact_format csv
```

### Install Wikipedia: List of S&P 500 companies data to PostgreSQL.

You need to setup PostgreSQL first. The [PostgreSQL and Metabase example](https://tsugumi-sys.github.io/stocklake/examples/postgresql_and_metabase/) might help you.

```bash
stocklake download wikisp500 --store_type postgresql
```

### Install Wikipedia: List of S&P 500 companies data and output as a serialized json to the standard output.

```bash
stocklake download wikisp500
```

## License

`stocklake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
