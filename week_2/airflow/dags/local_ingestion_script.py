import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as pg
import os

def data_ingest_to_db(user, password, host, port, db, table_name, csv_name, execution_date):

    print(table_name, csv_name, execution_date)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print('connection to the database successful, inserting data ...')
    
    # read in first 1000 rows to create db schema
    df = pd.read_csv(csv_name, nrows=1000, index_col=None)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    pd.io.sql.get_schema(df, name=table_name, con=engine, schema='postgres')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    conn = pg.connect(f'host={host} dbname={db} user={user} password={password}')
    cur = conn.cursor()
    with open(csv_name, 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, table_name, sep=',', null="")

    conn.commit()

    print(f'Data inserted into {db}.')
