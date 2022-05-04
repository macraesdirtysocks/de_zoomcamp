# 1. Introduction

These are some notes that helped me through week 2.  I spent a lot of time with github and getting everything setup on my VM.

To be clear I cloned my own repo to my VM and I'm running exclusivly from my VM now via VS Code which Alexey explained in video 1.4.1 @ 18:15 minute mark.

I decided to clone my own repo and do as much of my own work as possible instead of basically copying the instructors and just changing a couple variables.  This lead to a many problems but solving them is where you learn wtf is going going on.

- [1. Introduction](#1-introduction)
  - [1.1. Setup google credentials](#11-setup-google-credentials)
  - [1.2. Airflow Setup](#12-airflow-setup)
  - [1.3. Docker Build](#13-docker-build)
  - [1.4. Docker Compose](#14-docker-compose)

The first problem I ran into was reapeated and I still haven't come across a permanent fix.  I kept having to change the ownership of the de_zoomcamp folder on the VM everytime I started it.

```bash
# <user> = name you used when you generated your ssh key.
sudo chown -R <user> de_zoomcamp
```

## 1.1. Setup google credentials

Following along the official instructions I made a directory and sftp'd my credentials to my VM.

I followed these steps:

1. On the VM

    ```bash
       cd ~ && mkdir -p ~/.google/credentials/
    ```

2. On my local machine.

    ```bash

    # Navigate to where you credentials live.
    cd path/to my credentials/

    # Rename credentials if necessary
    mv <credentials file name> google_credentials.json

    # 
    sftp <'name you gave in your .config file for ssh into VM'>
    ```

3. Back on the VM

    After running sftp command you will be connected to VM at the sftp prompt.  It will look like sftp>.

    You can now navigate to where you want to transfer your credentials, probably the directory you creadted in step one.

    ```bash
    cd ~/.google/credentials/
    ```

4. To transfer the file using put

    ```bash
        put google_credentials.json
    ```
## 1.2. Airflow Setup

I followed along this part faily verbatim.

1. Create a new sub-directory called airflow in your project dir (such as
the one we're currently in)

2. Set the Airflow user:

    ```bash
    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

3. Import the official docker setup file from the latest Airflow version.

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

## 1.3. Docker Build

1. Create a Dockerfile pointing to Airflow version you've just downloaded, such as apache/airflow:2.2.3, as the base image.

2. Customize requirements.txt

Create a file called requirements.txt open it a list all the packages to install via pip install.

Doing this before you first build your image will save you some time.

My requirements.txt looks like this.
```python
apache-airflow-providers-google
pyarrow
sqlalchemy
pandas
psycopg2
```

## 1.4. Docker Compose

Back in your docker-compose.yaml, this is the template downloaded via curl in Airflow setup #3.

1. In x-airflow-common
    Remove the image tag, to replace it with your build from your Dockerfile

2. Mount your google_credentials in volumes section as read-only

3. Set environment variables as per your config: 
    - GCP_PROJECT_ID
    - GCP_GCS_BUCKET
    - GOOGLE_APPLICATION_CREDENTIALS
    - AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT

> I struggled mightily with the following.  There's something going on in all the setup but on the line where you mount your google credentials prefix it with /opt/airflow as I did below.

```yaml
volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    - ~/.google/credentials/:/opt/airflow/.google/credentials:ro
```

After spinning up your containers with docker-compose up you can check if your credentials are being mounted by connecting to the worker:

1. Get airflow worker id.

     ```bash
    # Copy the process id of the worker
    docker ps
    ```

2. Connect to worker.

    ```bash
    # Worker id from step 1.
    docker exec -it <worker id> bash
    ```

3. credentials should be there in .google/credentials/.

Here's how the final versions of your [Dockerfile](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/Dockerfile) and [docker-compose.yml](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/docker-compose.yaml) should look.

From here on in its pretty straight forward.  I create 3 DAG's using the DAG template from the course repo and put my own touches on them.  I would recommend adding in a clean up task however.

```bash

rm_task = BashOperator(
        task_id="delete_local_datasets",
        bash_command= f"rm {path_to_local_home}/{dataset_file} {path_to_local_home}/{parquet_file}"
    )

    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task >> rm_task
```

I have a couple issues I haven't figured out yet:

1. Dags seem to insist on trying to do a run for the current date even though I used a start_date and end_date.

2. I feel like when I have a start and end schedueled and catchup=True I should be able to see all the dags in the airfloww tree schedueled and ready to go.  However they just seem to genereate as they go.  Seems off.
