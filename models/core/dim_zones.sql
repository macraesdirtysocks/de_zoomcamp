{{ config(materialization='table') }}

select 
    location_id
    , borough
    , zone
    , replace({{ update_airport_code("zone", "service_zone") }}, 'Boro', 'Green') as service_zone
from {{ ref('taxi_zone_lookup') }}