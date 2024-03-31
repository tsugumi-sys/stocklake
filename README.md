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

## Setup Database

Stocklake only supports PostgreSQL.

You can use official PostgreSQL container. For example;

```yaml
# docker-compose.yml
version: '3'

services:
  db:
    image: postgres:16
    container_name: postgres
    ports:
      - 5432:5432
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: stocklake

volumes:
  postgres_data:
```

And run the following command:

```sh
docker compose up -d
```

## License

`stocklake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
