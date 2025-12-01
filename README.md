# catch-a-ride
Get status on New York City public transit routes

## Goal

For a given subway line, station on that line, direction of the train, and number of arrivals to check ahead - find the time until that train's next X arrivals. Present the data such that it more accessible for on-demand queries of fixed station arrival times than the MTA app or other route planning services (e.g., Google Maps) by making the service queryable by home automation services.

## Source Data

- GTFS Protobuf file - https://github.com/google/transit/blob/master/gtfs-realtime/proto/gtfs-realtime.proto
- MTA-specific data - https://www.mta.info/developers
  - MTA Protobuf file - https://raw.githubusercontent.com/OneBusAway/onebusaway-gtfs-realtime-api/master/src/main/proto/com/google/transit/realtime/gtfs-realtime-NYCT.proto
  - MTA feed referece - https://www.mta.info/document/134521
  - MTA static subway data - https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip

## TODO

### Create a network diagram for the suggested setup

The description of the Goal has been expanded to show a value-add over using existing services that already pull from the same data set and have features not yet created for this service like alert notes. A diagram to visualize this desired flow should be created to aid in showing the project's value with an example use case.

Example to diagram:
1. User speaks a key phrase (e.g., 'when does my train get here?') to a home assistant
2. The home assistant translates the key phrase to an API call, with known input for a specific request, to a host on the local network running `catch-a-ride`
3. `catch-a-ride` returns subway data in a conversational format (e.g., 'The next 1 trains are in 6, 14, and 22 minutes') as the response of the API call
4. The home assistant plays the API response on a speaker on the home automation network

### Optimize deduplication of stop IDs for single direction

The function `split_directionality_and_dedupe` in `src/mta_stops_to_stations.py` always returns two dicts for the give line(s) and does not consider the case when only one direction is needed. The above function should take a direction argument and return only one dictionary for the given direction.
Complexity of the function will remain the same as it must currently iterate through all content regardless, but it will simplify calls in the main script and avoid having to build a dict that goes unused.

### Explicitly deprecate the stations per line file in /data 

`data/stations_per_line.json` was collected at a time when (luckily) the Z train was in service and there were no active alerts for trains skipping stations -- with the assumption that all subway lines had trip data for every stop along their normal service path. This does not account for weekend/modified service and can lead to inaccurate/unhelpful output under certain conditions (e.g., checking for late night service, or reroutes caused by unplanned maintenance).
Add a disclaimer that the saved data applies only to regular service for mapping purposes.

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