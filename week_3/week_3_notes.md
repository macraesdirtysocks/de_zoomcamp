# Week 3 notes

I decided to rock separate dags for the fhv and yellow taxi data.  The dags are essentially copies of each other with some file names changed.

One thing I would suggest is to omit ```move_object=True``` from the code beacuse if you make a mistake it can mess with your data and you may have to redo week 2 to get it back.  Omitting this part will copy the files instead of moving them.

I made a mistake when moving the files where I didn't use the correct sytax in naming the destination file and they were all named the same so I had to re run the week 2 dags to get my data back.

Specifically using a wildcard in the naming which is described in the [GCSToGCSOperator destination_object param](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/transfers/gcs_to_gcs/index.html).

So if your dag runs keep failing go to your stogae bucket and make sure the data hasn't been moved and the filename altered by the move.

Use these commands from the command line to quickly check your gcs:

```bash

# Get list of buckets
gsutil ls

# Get get content in specific bucket
gsutil ls <bucket name> 

# Get get content of folder in bucket
gsutil ls <bucket name>/<folder>
```

Odds are if folders other than 'raw' exist then something happened to your data.

If you make this mistake this code can help as long as the files are still distinguishable.

```bash
# Move data back to original folder
gsutil mv gs://<bucket name>/<folder containing data>/<filename prefix>*.parquet gs://<bucket name>/<folder to move data back to>/
```

I'm really racking my brain to include more in here but I have experience with this type of work and I really had no trouble completing this week at all.
