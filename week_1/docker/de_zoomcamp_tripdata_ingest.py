import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as pg
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    df = pd.read_csv(csv_name, nrows=1000, index_col=None)


    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    pd.io.sql.get_schema(df, name=table_name,con=engine, schema='postgres')


    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)


    conn = pg.connect("host=localhost dbname=ny_taxi user=root password=root")
    cur = conn.cursor()
    with open(csv_name, 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, table_name, sep=',', null="")

    conn.commit()

    print(f'Data inserted into {db}.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inget csv data to Postgres')

    parser.add_argument('--user', help='username for pg')
    parser.add_argument('--password', help='password for pg')
    parser.add_argument('--host', help='host name for pg')
    parser.add_argument('--port', help='port for pg')
    parser.add_argument('--db', help='db name for pg')
    parser.add_argument('--table_name', help='table name for writting data to')
    parser.add_argument('--url', help='url for csv data')

    args = parser.parse_args()

    main(args)