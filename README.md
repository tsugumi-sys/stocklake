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

## Supported APIs

| name | status | API Docs | Additional Information |
| :--- | :---: | :--- | :--- |
| Nasdaq API (Screener) | ✅ | [URL](https://www.nasdaq.com/market-activity/stocks/screener) | |
| Polygon API (Stock Financials Vx) | ✅ | [URL](https://polygon.io/docs/stocks/get_vx_reference_financials) | [Data Fields Information](https://polygon.io/blog/financials-api-glossary-of-fields) |
| Polygon API (Tickers) | ✅  | [URL](https://polygon.io/docs/stocks/get_v3_reference_tickers) | |
| Wikipedia: List of S&P 500 companies | ✅ | [URL](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) |  |

## Examples

### Nasdaq API (Screener)

```bash
stocklake download nasdaqapi --exchange nasdaq --store_type postgresql
```

### Polygon API (Stock Financials Vx)

```bash
stocklake download polygonapi stock-financials-vx --symbols AAPL --store_type postgresql
```

### Wikipedia: List of S&P 500 companies

```bash
stocklake download wikisp500 --store_type postgresql
```


## License

`stocklake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
