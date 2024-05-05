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

Then, copy the docker compose file contents from this repository and run docker containers.

```sh
docker compose up -d
```

This command builds the following containers.

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
| :----: | :----: |
| Database Type | `PostgreSQL` |
| Host | `stocklake-db` |
| Port | `5432` |
| Database name | `stocklake` |
| Username | `postgres` |
| Password | `password` |

Other settings can be theier default values.

## License

`stocklake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
