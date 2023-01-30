import argparse
import os
from time import time

import pandas as pd
from sqlalchemy import create_engine



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db 
    table_name = params.table_name 

    # Connect to database
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    os.system(f"wget {url} -O output.csv")
    
    df_iter = pd.read_csv("output.csv", iterator=True, chunksize=100000)
    
    while True:
        t_start = time()

        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name = table_name,
            con=engine,
            if_exists="replace")

        t_end = time()

        print("Inserted another chunk..., took %.3f seconds" % (t_end - t_start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("user", help="user name for postgres")
    parser.add_argument("pass", help="password for postgres")
    parser.add_argument("host", help="host for postgres")
    parser.add_argument("port", help="port for postgres")
    parser.add_argument("db", help="database name for postgres")
    parser.add_argument("table-name", help="name of the table where we will write the results to")
    parser.add_argument("url", help="url of the csv file")
    parser.add_argument("file", help="Path to the csv file")    
    args = parser.parse_args()

    
    main(args)
