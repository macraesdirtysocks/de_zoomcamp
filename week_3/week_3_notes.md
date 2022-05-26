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

LOL at that last statement.  A couple weeks later I'm back to week 3.  For some reason I downloaded yellow taxi data and the FHV (For-hire-vehicles) only to get to week 4 and Victoria is working with yellow and green, not yellow and FHV.  So I came back to week 3 to replace the FHV data with the green taxi data and what did I find?  The taxi website switched to parquet files! Yay right!? Well I went ahead and took out all the csv to parquet stuff and though I was styling.  Switched back to week 4 only to run into major headaches.

If you ran into the same problems and now you're here welcome.  

I actually had to go back to week 2 because it seemed easier to work with the parquet files during rather than after ingestion.

Turns out there are different data types for some of the columns across the parquet fiels which causes a hastle when creating the tables in week 4.  Specifically in the green data the problem is in the `ehail_fee` column and `airport_fee` in the yellow data.  The columns are a mix of string and numeric types acros columns which don't play well together.  If you check my scripts you will see I added a scheam_update function which converts these columns to numeric.  I didn't get too fancy with it so theres's more work being done than needed but it works.

So to use my code you will need the two schema.json files.  The dags have a few things different about them so take care to note the modules, variables and diffent tasks.  

Note that my dags will not create `trips_data_all` dataset so you need to do that from the concole or command line.  There is an airflow operator for it but I didn't bother.
