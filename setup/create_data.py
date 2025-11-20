import csv
from collections import defaultdict
import json

def load_stops_maps(csv_file="data/stops.csv") -> tuple[defaultdict[list], dict[str]]:
    """
    Loads the stops.csv file (from https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip) and translate it into dictionaries for bidirectional mapping.
    
    Args:
        csv_file: The path to a CSV file containing "stop_id" and "stop_name" columns
    
    Returns:
        name_to_ids_map: A defaultdict of lists of strings, with keys as the human-readable names of a station and values as a list of machine-readable station IDs
        id_to_name_map: A dict of strings, with keys as a list of machine-readable station IDs and values as the human-readable names of a station
    """
    name_to_ids_map = defaultdict(list)
    id_to_name_map = {}
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stop_name = row.get('stop_name')
                stop_id = row.get('stop_id')
                if stop_name and stop_id:
                    # Map '23 St' to ['130', 'A30', 'R19', 'N09S', ...]
                    name_to_ids_map[stop_name].append(stop_id)
                    # Map 'N09S' to '23 St'
                    id_to_name_map[stop_id] = stop_name
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        return None, None
    return name_to_ids_map, id_to_name_map

station_name_to_station_ids, station_id_to_station_name = load_stops_maps()
with open('data/name_to_ids.json', 'w') as f:
    json.dump(dict(station_name_to_station_ids), f, indent=2)
with open('data/id_to_name.json', 'w') as f:
    json.dump(station_id_to_station_name, f, indent=2)