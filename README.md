# catch-a-ride
Get status on New York City public transit routes

## Goal

For a given subway line, station on that line, direction of the train, and number of arrivals to check ahead - find the time until that train's next X arrivals.

## Source Data

- GTFS Protobuf file - https://github.com/google/transit/blob/master/gtfs-realtime/proto/gtfs-realtime.proto
- MTA-specific data - https://www.mta.info/developers
  - MTA Protobuf file - https://raw.githubusercontent.com/OneBusAway/onebusaway-gtfs-realtime-api/master/src/main/proto/com/google/transit/realtime/gtfs-realtime-NYCT.proto
  - MTA feed referece - https://www.mta.info/document/134521
  - MTA static subway data - https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip

## TODO

### Discard past arrival times

In certain cases, stale data may be present in the API output that leads to showing invalid arrival times (e.g., a file written at timestamp '1763604000' contained an arrival time '1763599950', leading to an output of "Train arriving in -67 minutes"). The function `find_next_arrival_times` should take `current_time` as an arguemnt and only append `i['arrival']['time']` if it is greater than `current_time`.

### Do not rely on /data for stations per line

`data/stations_per_line.json` was collected at a time when (luckily) the Z train was in service and there were no active alerts for trains skipping stations -- with the assumption that all subway lines had trip data for every stop along their normal service path. This does not account for weekend/modified service and can lead to inaccurate/unhelpful output under certain conditions (e.g., checking for late night service, or reroutes caused by unplanned maintenance).
Consider a disclaimer that the saved data applies only to regular service for mapping purposes, and switch to performing real-time station lookups for live service.

### Add detailed setup instructions

The current `setup/create_stops_to_stations_map.py` execution errors when trying to find the path to `import src.mta_subway_fetcher`. This can be mitigated by moving `create_stops_to_stations_map.py` up one directory level and running it.
Resolving this is low priority -- `create_stops_to_stations_map.py` should be deprecated as a setup step by the above TODO item, and until then is a one-time required setup that creates the already-present file `data/stations_per_line.json`.

### Documentation & Validation

Continue function definitions and adding comments.
Continue validating user input and add test cases.

## Future Goals

- Multiple route/station selections to support transfers
- Include alert messages
- Extend to MTA buses