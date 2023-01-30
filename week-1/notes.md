
# Setup docker

## Postgres container

```sh
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $HOME/_tmp/zoomcamp-2023/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --name zoomcamp-postgres \
    postgres:13-alpine
```

Connect to the database 
```sh
pgcli -h localhost -U root -d ny_taxi 
```

