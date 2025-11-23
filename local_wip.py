import src.mta_subway_fetcher as mta_subway_fetcher
import src.mta_stops_to_stations as mta_stops_to_stations

from datetime import datetime
from collections import defaultdict
import json

def get_subway_selection(realtime_stations: bool=True) -> tuple[str, str, str, int]:
    """
    Prompt the user to select a subway line, station, and direction
    
    Args:
        realtime_stations: Whether to fetch real-time station data (True, default) or use cached standard stops (False)
        *addditional data collected by user input
    
    Returns:
        input_line: A string representing the chosen subway line
        input_direction: A string representing the chosen direction (uptown/northbound or downtown/southbound)
        input_station_id: A string representing the chosen subway station
        input_count: An integer, between 1 and 5, representing the count of upcoming subway lines to return
    """
    input_validator = True
    while input_validator:
        print(mta_subway_fetcher.SUBWAY_LINE_LIST)
        input_line = str(input("Input one of the above options to specify the subway line, where 'Sr' is the Rockaway Park Shuttle and 'Sf' is the Franklin Avenue Shuttle (defaults to the '1' train): ") or "1")
        if input_line in mta_subway_fetcher.SUBWAY_LINE_LIST:
            input_validator = False
        else:
            print(f"Input {input_line} is not valid, please select a character in the presented range.")
    
    input_validator = True
    while input_validator:
        input_direction = str(input("Select 'N' for Northbound/Uptown or 'S' for Southbound/Downtown (defaults to 'S'): ") or "S")
        if input_direction in ["N", "S"]:
            input_validator = False
        else:
            print(f"Input {input_direction} is not valid, please select N or S.")

    # Create the list of available subway stations IDs, either from real-time data or cached standard weekday service stops
    if realtime_stations:
        realtime_stops_for_lines = mta_stops_to_stations.get_stops_for_lines([input_line])
        selected_line_station_ids_dict = mta_stops_to_stations.remove_directionality_and_dedupe(realtime_stops_for_lines)
        selected_line_station_ids = selected_line_station_ids_dict[input_line]
    else:
        with open('data/stations_per_line.json', 'r') as f:
            all_stations = json.load(f)
        selected_line_station_ids = all_stations[input_line]

    # Convert stop IDs to human-readable station names
    with open('data/id_to_name.json', 'r') as f:
        all_station_names = json.load(f)
    selected_line_stations = defaultdict(str)
    for id in selected_line_station_ids:
        selected_line_stations[all_station_names[id]] = id

    input_validator = True
    while input_validator:
        print(list(selected_line_stations.keys()))
        input_station = str(input("Select a station from the above list (defaults to the first value): ") or next(iter(selected_line_stations)))
        if input_station in selected_line_stations.keys():
            input_validator = False
            input_station_id = selected_line_stations[input_station]
            print(f"Station id for '{input_station}' is {input_station_id}")
        else:
            print(f"Input {input_station} is not valid, please select from the list.")
    
    input_validator = True
    while input_validator:
        input_count = int(input("Select the next number of train arrival times to return (defaults to 3): ") or 3)
        if isinstance(input_count, int) and 0 < input_count < 6:
            input_validator = False
        else:
            print(f"Input {input_count} is not valid, please select a whole number between 1 and 5.")
        
    return input_line, input_direction, input_station_id, input_count

def fetch_data_from_input(subway_line: str) -> dict:
    """
    Collect input from the user to fetch real-time data for the selected subway line.

    Args:
        subway_line: A string representing the chosen subway line

    Returns:
        subway_data: A dict of MTA real-time data for the subway line group of the desired line (e.g., 1/2/3/4/5/6/7/S for input '1')
    """
    subway_data = mta_subway_fetcher.get_realtime_data(subway_line)
    output_filepath = f'tmp/{subway_line}_group-data.json'
    with open(output_filepath, 'w') as f:
        json.dump(subway_data, f, indent=2)
    return subway_data

def extract_subway_line(subway_line: str, subway_group_dict: dict) -> dict:
    """
    For real-time data on a given group of subway lines, extract only the desired subway line.
    
    Args:
        subway_line: A string representing the chosen subway line
        subway_group_dict: A dict of MTA real-time data for the subway line group of the desired line (e.g., 1/2/3/4/5/6/7/S for input '1')
    
    Returns:
        line_stats: The input dict 'subway_group_dict' with the value in 'entity' filtered down to only the chosen subway line. Note that the 'header' values still contain Route IDs for the entire group, although these values are unused.
    """
    line_stats = {'header': None, 'entity': []}
    line_stats['header'] = subway_group_dict['header']
    for e in subway_group_dict['entity']:
        if e.get('tripUpdate') and e['tripUpdate'].get('stopTimeUpdate') and e['tripUpdate']['trip']['routeId'] == subway_line:
            line_stats['entity'].append(e)
    output_filepath = f'tmp/{subway_line}.json'
    with open(output_filepath, 'w') as f:
        json.dump(line_stats, f, indent=2)
    return line_stats

def find_next_arrival_times(subway_lines_stats: dict, direction: str, station_name: str, next_x_trains: int, current_time: int) -> list[int]:
    """
    For a given subway line's data, a direction, and a station stop, find the next X arrival times.
    
    Args:
        subway_lines_stats: A dict of MTA real-time data for the chosen subway line
        direction: A string representing the chosen direction (uptown/northbound or downtown/southbound)
        station_name: A string representing the chosen subway station
        next_x_trains: An integer representing the count of upcoming subway lines to return
        current_time: An integer representing the current epoch time (converted from float to match MTA output)
    
    Returns:
        arrival_times: A list of integers representing arrival times of upcoming trains, in Epoch time
    """
    full_station_name = station_name + direction
    inc = 0
    arrival_times = []
    for e in subway_lines_stats['entity']:
        if inc >= next_x_trains:
            break
        for i in e['tripUpdate']['stopTimeUpdate']:
            if i['stopId'] == full_station_name and int(i['arrival']['time']) > current_time:
                arrival_times.append(int(i['arrival']['time']))
                inc += 1
    return arrival_times

def main():
    subway_line, direction, station, count = get_subway_selection()
    
    subway_group_stats = fetch_data_from_input(subway_line)
    subway_line_stats = extract_subway_line(subway_line, subway_group_stats)
    
    current_time = int(datetime.now().timestamp())
    next_train_times = find_next_arrival_times(subway_line_stats, direction, station, count, current_time)

    for i in next_train_times:
        print(f"Train arriving in {int((i-current_time) / 60.0)} minutes")

main()