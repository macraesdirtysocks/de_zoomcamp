import os
import logging
from datetime import datetime


from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator, BigQueryCreateEmptyTableOperator, BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
INPUT_FOLDER = "raw"
INPUT_FILETYPE = "parquet"
INPUT_FILENAME = "green_tripdata"
OUTPUT_FOLDER = "green"
DS_COLUMN = "lpep_pickup_datetime"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')
EXTERNAL_TABLE_SCHEMA = "green_tripdata_schema.json"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="green_taxi_data_ingestion_gcs_dag",
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    max_active_runs=3,
    tags=['de-zoomcamp'],
) as dag:

    green_gcs_to_gcs_sort_task = GCSToGCSOperator(
            task_id='copy_files',
            source_bucket=BUCKET,
            source_object=f'{INPUT_FOLDER}/{INPUT_FILENAME}*.{INPUT_FILETYPE}',
            destination_bucket=BUCKET,
            destination_object=f'{OUTPUT_FOLDER}/{INPUT_FILENAME}'
        )

    bq_green_tripdata_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bq_green_tripdata_external_table_task",
        destination_project_dataset_table=f"{PROJECT_ID}.{BIGQUERY_DATASET}.{INPUT_FILENAME}_external_table",
        bucket=BUCKET,
        source_objects=[f'{OUTPUT_FOLDER}/*'],
        schema_object=EXTERNAL_TABLE_SCHEMA,
        source_format=INPUT_FILETYPE
    )

    CREATE_BQ_TBL_QUERY = (
            f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{INPUT_FILENAME} \
            PARTITION BY DATE({DS_COLUMN}) \
            AS \
            SELECT * FROM {BIGQUERY_DATASET}.{INPUT_FILENAME}_external_table;"
        )

    # Create a partitioned table from external table
    bq_create_partitioned_table_job = BigQueryInsertJobOperator(
        task_id=f"bq_create_{INPUT_FILENAME}_partitioned_table_task",
        configuration={
            "query": {
                "query": CREATE_BQ_TBL_QUERY,
                "useLegacySql": False,
            }
        }
    )

    green_gcs_to_gcs_sort_task >> bq_green_tripdata_external_table_task >> bq_create_partitioned_table_job
    