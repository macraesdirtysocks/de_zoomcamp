# Docker setup
These are some notes from my wading through the docker/sql portion of week 1.

The first thing that really tripped me up was not having docker running on my computer.  You probably installed it already but I didn't quite catch that you need to have it running on your local machine.

TLDR - make sure you have the docker icon in your menu bar.

The general progression in docker is Dockerfile > Image > Container.

- [Docker setup](#docker-setup)
  - [Make a Dockerfile](#make-a-dockerfile)
  - [Create pipeline.py](#create-pipelinepy)
  - [Run docker](#run-docker)
  - [Command line postgres tool](#command-line-postgres-tool)
  - [Ingest taxi dataset](#ingest-taxi-dataset)
  - [pgAdmin and docker](#pgadmin-and-docker)
  - [Docker Compose](#docker-compose)



## Make a Dockerfile

The dockerfile has to be called 'dockerfile' or 'Dockerfile' but 'Dockerfile' is convention.   Not 'dockerfile.dockerfile', not 'my_dockersetup.dockerfile', don't use any file extentions.  Just 'Dockerfile'.

Here is what the contents of Dockerfile should be:

```python
# dockerfile

# The base image
FROM python:3.9.1 

# Install python packages
RUN pip install pandas 

# Create a directory named app.
WORKDIR /app 

# Copy pipeline.py on local to pipeline.py in docker.
COPY pipeline.py pipeline.py 

# What to do when docker run command is executed.
# This will enter python and run pipeline.py.
ENTRYPOINT [ "python", "pipeline.py" ] 
```

## Create pipeline.py

```python
# pipeline.py

import sys
import pandas as pd
print(sys.argv)
day = sys.argv[1]
# some fancy stuff with pandas

print(f'job finished successfully for day = f{day}')
```

## Run docker

I want to clarify the -it / -d options.  They get frequent use and I wasn't 100% on them.

Imagine the following commands

```docker
    docker run -it ubuntu

    docker run -d ubuntu
```

-it puts you in the container at the bash command line where you can run linux commands.

-d starts the container but you are not inside it and unable to run bash commands.

Make sure you have the $(pwd) part in the folder mapping.  Copy and paste this into your terminal.

```python
docker run -it \
 -e POSTGRES_USER="root" \
 -e POSTGRES_PASSWORD="root" \
 -e POSTGRES_DB="ny_taxi" \
 -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
 -p 5432:5432 \
 postgres:13
```

If you get an error about the port being in use:

``` python

# Run this in the terminal.
sudo lsof -i tcp:5432

# Note the PID.

# Run this in the terminal.
kill <PID>

# Rerun the docker run -it bit from above.
```

After docker is up and running you can't do anything else in the terminal window where the docker run command was executed.  This hung me up for a little bit.  Open a new terminal window.

If you want to double check things went well you can check your working directory for the ny_taxi_postgres_data.  It'll have a bunch of postgres files in there.  Leave them be.

## Command line postgres tool

The course reccommends pgcli.

```python
pip3 install pgcli
```

I have been using psql in the past so I stuck with that.  If I'm not mistaken psql comes installed with postgres.

Connecting to the database:

```python
# pgcli
pgcli -h localhost -p 5432 -U root -d ny_taxi
```

```python
# postgres
psql -h localhost -p 5432 -U root -d ny_taxi
```

In this next section we will be looking at the taxi dataset doing a tinsy bit of EDA but this part is mostly about ingesting the dataset into the database.

I personally use jupyter lab but you can use whatever you want.

## Ingest taxi dataset

Get the csv

```bash
# Download taxi csv data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

Each of the following code blocks is a cell in jupyter.

```python
# import modules
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as pg
```

```python
# create an engine.
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```

I used index_col=none because I didn't think it was necessary.  

It is important to set nrows to a number in the thousands because it helps determine datatypes of the columns.  Initally I only read in a few columns and it auto guessed the wrong column types and that messed up the schema.  The error occured specifically in `tolls_amount` setting it to int64.  After reading more rows it is changed to float64.

```python
# Read csv into a df.
df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=1000, index_col=None)
```

Convert the pickup and dropoff times to datetime.

```python
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# Check the column data types.
display(df.info())
```

Preview the schema.

```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data',con=engine, schema='postgres'))
```

```python
df.head().to_sql(name='yellow_taxi_data', con=engine, if_exists='replace', index=False)
```

Here's were I took a major shortcut.  Instead of copying the entire dataset into a df and interating I just copied the csv straight to the database.

I would like to call attentoion to `null=""` argument.  This is necessary because some of the data is missing and the copy will fail.  Specifically a line deep in the dataset has a `VendorID = ""` and this casues the copy to fail because `""` is an empty string which violate the schema which says `VendorID` is type int64.  

This comes from the psycopg documentation for [copy_to](https://www.psycopg.org/docs/cursor.html).

```python
conn = pg.connect("host=localhost dbname=ny_taxi user=root password=root")
cur = conn.cursor()
with open('yellow_tripdata_2021-01.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.

    cur.copy_from(f, 'yellow_taxi_data', sep=',', null="")

conn.commit()
```

Now if we go back to our terminal and connect to our database using one of the connections outline in section 4 we can execture an SQL statement and see we have.

```SQL
SELECT COUNT(1) FROM yellow_taxi_data;
```

## pgAdmin and docker

In section 3 we ran a postgres database inside of a container using the code below.

```python
docker run -it \
 -e POSTGRES_USER="root" \
 -e POSTGRES_PASSWORD="root" \
 -e POSTGRES_DB="ny_taxi" \
 -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
 -p 5432:5432 \
 postgres:13
```

We interacted with database a bit by connecting to it via psql or pgcli adn now we want to use pgAdmin to explore the data.

If we just fire up another container running pgAdmin it won't work because the database and pgAdmin are in their own isolated containers I'm not entirely sure why this is.

So whats the solution? Well we need to create a network.  Think of it like individual boxes.  The db is a box and pgAdmin is a box, now we need to put them together in a bigger box.

Run these commands in separate terminals

1. Terminal 1

```python
# terminal 1
docker run -it \
 -e POSTGRES_USER="root" \
 -e POSTGRES_PASSWORD="root" \
 -e POSTGRES_DB="ny_taxi" \
 -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
 -p 5432:5432 \
--network=pg-network \
--name pg-database \
 postgres:13
```

2. Terminal 2

```bash

# terminal 2
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

3. Terminal 3
 
```bash

URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

python3 de_zoomcamp_tripdata_ingest.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \
  --url=$URL

```

1. Terminal 4

```python
# terminal 3
# command should open defualt browser to pgadmin login.
open 'http://localhost:8080'
```

## Docker Compose

Well that was a lot to get the conatiners running and connect to pgadmin.  Isn't there a way to do all that in one go? Yes there is, with docker compose.  Docker compose should be on you system already as part of docker.

```python
# Check if docker compose is on your system.
docker-compose 
```

Now we create docker compose file which is written in yml or yaml.  YAML is a data storage as code language simialr to json or XML but is very human readable.  It is used to write configuration files like we will be doing here.  

The following should be the contents of your docker-compose file.

```yml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
```

You need to be in same directory for the docker-compose command to work.

```python
# Spin up the containers
docker-compose up

# Check that the containers are running.
docker ps

# login into pgadmin
open 'http://localhost:8080'
```

Log in like before and away you go.
