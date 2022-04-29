from datetime import datetime
from airflow import DAG
import os

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from local_ingestion_script import data_ingest_to_db


path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
URL_BASE = 'https://s3.amazonaws.com/nyc-tlc/trip+data' 
URL_TAIL = '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
URL = URL_BASE + URL_TAIL
OUTPUT_FILE_PATH = path_to_local_home + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
TABLE_NAME = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')


local_workflow = DAG(
    dag_id="local_ingestion_dag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1,)

)

with local_workflow:

    wget_task = BashOperator(
        task_id='download_data',
        bash_command=f'curl -sS {URL} > {OUTPUT_FILE_PATH}/{TABLE_NAME}'
    )

    ingestion_task = PythonOperator(
        task_id='ingest_data',
        python_callable=data_ingest_to_db,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME,
            csv_name=OUTPUT_FILE_PATH
        ),
    )

    wget_task >> ingestion_task
