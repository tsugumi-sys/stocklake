## About

We can use PostgreSQL database to store data.

## Setup

### 1. prepare PostgreSQL instance

You can use PostgreSQL container to create instance in your machine.

For example;

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

### 2. Set environment variable

You can set the following variables in `.env`.

If you use the above docker compose setup, you can skip this step.

```sh
STOCKLAKE_POSTGRES_HOST=localhost
STOCKLAKE_POSTGRES_USER=postgres
STOCKLAKE_POSTGRES_PASSWOR=password
STOCKLAKE_POSTGRES_DATABASE=stocklake

```

### 3. Run migration

```bash
stocklake db upgrade --revision head
```
