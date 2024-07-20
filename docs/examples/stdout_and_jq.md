## standard output and jq command example

Here is an example to download the all the S&P500 symbols financials data from Polygon Stock Financials Vx API to PostgreSQL.

```bash
stocklake download wikisp500 | jq -r 'map(.symbol) | join(",")' | xargs stocklake download polygonapi stock-financials-vx --store_type postgresql --symbols
```
