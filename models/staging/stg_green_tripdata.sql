{{config(materialized='view')}}

with tripdata as (
    select *
        , row_number() over(partition by VendorID, lpep_pickup_datetime) as rn
    from {{ source('staging', 'green_tripdata') }}
    where 
        VendorID is not null
)

select 
-- identifiers
    {{ dbt_utils.surrogate_key(['VendorID', 'lpep_pickup_datetime']) }} as trip_id
    , VendorID as vendor_id
    , cast(lpep_pickup_datetime as timestamp) as pickup_datetime
    , cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime

    -- trip info
    , passenger_count
    , trip_distance
    , trip_type
    , RatecodeID as ratecode_id
    , store_and_fwd_flag
    , PULocationID as pickup_location_id
    , DOLocationID as dropoff_location_id

-- cost info
    , cast(payment_type as int) as payment_type
    , {{ get_payment_type_description('payment_type') }} as payment_type_description
    , fare_amount
    , extra
    , mta_tax
    , tip_amount
    , tolls_amount
    , improvement_surcharge
    , congestion_surcharge
    , total_amount


from tripdata
where rn = 1