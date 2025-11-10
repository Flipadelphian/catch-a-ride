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

### Expand .data/

Create a `data/stations_per_line.json` file that lists all station IDs for a given subway line
```
with open('tmp/1.json', 'r') as f:
    1_stats = json.load(f)
for e in 1_stats['entity']:
    for i in e['tripUpdate']['stopTimeUpdate']:
        print(i['stopId'])
```
Replace `print(i['stopId'])` with "create a list of unique `stopId` values with their friendly name", repeat for each line, and merge into a `stations_per_line.json` file of format:
```
{ 
    'subway_line_x': [('stop_1_name', 'stop_id_1'), ('stop_2_name', 'stop_id_2'), ...],
    'subway_line_y': [('stop_1_name', 'stop_id_1'), ('stop_2_name', 'stop_id_2'), ...],
    ...
}
```

### Prompt for station

Extend `def get_subway_selection()` with a prompt to select the subway station for the given line, based on the available stops found for `subway_line_x` in `data/stations_per_line.json`.

### Streamline subway line selection

Remove the prompt for a subway group. End users get no benefit from selecting the MTA's subway grouping as they must select a specific subway line regardless - this extra step only creates friction.

Selecting a group may have a future benefit for a scenario like "give me all trains at this station that go to the same stop", but that scenario is out of scope at this time.

## Future Goals

- Multiple route/station selections to support transfers
- Include alert messages
- Extend to MTA buses