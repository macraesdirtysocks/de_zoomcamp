from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


local_workflow = DAG(
    dag_id="local_ingestion_dag",
    schedule_interval="0 6 2 * *"

)

with local_workflow:

    wget_task = BashOperator(
        task_id="download_data",
        bash_command='echo "data downloaded"'
    )

    ingestion_task = BashOperator(
        task_id="ingest_data",
        bash_commmand='echo "data ingested"'
    )

    download_data >> ingest_data

