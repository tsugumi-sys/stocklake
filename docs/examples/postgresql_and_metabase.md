## PostgreSQL and Metabase example

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
