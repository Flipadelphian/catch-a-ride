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

### Documentation

Continue function definitions and adding comments

### Validation

Continue validating user input and add test cases

### Do not rely on /data for stations per line

`stations_per_line.json` was collected at a time when (luckily) the Z train was in service and there were no active alerts for trains skipping stations -- with the assumption that all subway lines had trip data for every stop along their normal service path. This does not account for weekend/modified service and can lead to inaccurate/unhelpful output under certain conditions (e.g., checking for late night service, or reroutes caused by unplanned maintenance).
Consider a disclaimer that the saved data applies only to regular service for mapping purposes, and switch to performing real-time station lookups for live service.

## Future Goals

- Multiple route/station selections to support transfers
- Include alert messages
- Extend to MTA buses