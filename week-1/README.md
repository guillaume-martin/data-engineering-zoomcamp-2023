# Week 1 Homework

## Setup Postgres container

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


## Question 1. Knowing docker tags

Run the command to get information on Docker 
```
docker --help
```
Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

**Answer** =>  `--iidfile string`
 
## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

**Answer** => 3
```
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.


```sql
SELECT count(1)
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = '2019-01-15'
AND lpep_dropoff_datetime::date = '2019-01-15'
;
count|
-----+
20530|
```

**Answer** => 20530


## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28 
- 2019-01-15
- 2019-01-10

```sql
SELECT lpep_pickup_datetime::date, max(trip_distance)
FROM green_taxi_data
WHERE lpep_pickup_datetime::date IN ('2019-01-18', '2019-01-28', '2019-01-15', '2019-01-10')
GROUP BY lpep_pickup_datetime::date;
;
+----------------------+--------+
| lpep_pickup_datetime | max    |
|----------------------+--------|
| 2019-01-18           | 80.96  |
| 2019-01-15           | 117.99 |
| 2019-01-10           | 64.2   |
| 2019-01-28           | 64.27  |
+----------------------+--------+
```

**Answer** => 2019-01-15


## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?

```sql
WITH cte_trips AS (
     SELECT
         lpep_pickup_datetime::date as trip_date
         , passenger_count
         , count(1) AS trip_count
     FROM
         green_taxi_data
      WHERE 
          lpep_pickup_datetime::date = '2019-01-01'
     GROUP BY
         lpep_pickup_datetime::date
         , passenger_count
 )
 SELECT
     trip_date
     , passenger_count
     , trip_count
 FROM
     cte_trips
WHERE 
    passenger_count IN (2, 3)
;
trip_date |passenger_count|trip_count|
----------+---------------+----------+
2019-01-01|              2|      1282|
2019-01-01|              3|       254|
```

**Answer** => 2: 1282 ; 3: 254
 

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

```sql
SELECT 
    green_taxi_data.tip_amount
    ,zone_lookup.zone
FROM 
    green_taxi_data 
        LEFT JOIN zone_lookup 
            ON green_taxi_data."DOLocationID" = zone_lookup.location_id
WHERE 
    "PULocationID" = 7
ORDER BY 
    tip_amount desc;
tip_amount|zone                         |
----------+-----------------------------+
      88.0|Long Island City/Queens Plaza|
      30.0|Central Park                 |
      25.0|NA                           |
```

**Answer** => Long Island City/Queens Plaza



