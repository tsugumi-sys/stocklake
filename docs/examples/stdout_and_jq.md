## standard output and jq command example

pre requesties:
- [install jq](https://jqlang.github.io/jq/download/)

Here is an example to download the all the S&P500 symbols financials data with an interval of 30 seconds from Polygon Stock Financials Vx API to PostgreSQL.

```bash
stocklake download wikisp500 | jq -r 'map(.symbol) | join(",")' | xargs stocklake download polygonapi stock-financials-vx --store_type postgresql --interval_sec 30 --symbols
```
