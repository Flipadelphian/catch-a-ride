import src.mta_subway_fetcher as mta_subway_fetcher

from datetime import datetime
from zoneinfo import ZoneInfo
import json

def get_subway_selection() -> tuple[int, str, str]:
    """
    Prompt the user to select a subway line, station, and direction
    """
    input_validator = True
    while input_validator:
        for i in range(len(mta_subway_fetcher.SUBWAY_SELECTOR_MAP)):
            print(f'[{i+1}] = Subway lines {mta_subway_fetcher.SUBWAY_SELECTOR_MAP[i]}')
        input_int = int(input('Select a number from the subway groups above (defaults to 5 --> NQRW): ') or 5)
        if input_int-1 in range(0, len(mta_subway_fetcher.SUBWAY_SELECTOR_MAP)):
            input_validator = False
        else:
            print(f"Input {input_int} is not valid, please select a number in the presented range.")
    
    input_validator = True
    while input_validator:
        subway_options = mta_subway_fetcher.SUBWAY_SELECTOR_MAP[input_int-1]
        print(subway_options)
        input_line = str(input("Select one of the above characters to specify the subway line (defaults to the first subway line):") or subway_options[0])
        if input_line in subway_options:
            input_validator = False
        else:
            print(f"Input {input_line} is not valid, please select a character in the presented range.")
    
    input_validator = True
    while input_validator:
        input_direction = str(input("Select 'N' for Northbound/Uptown or 'S' for Southbound/Downtown (defaults to 'S'):") or "S")
        if input_direction in ["N", "S"]:
            input_validator = False
        else:
            print(f"Input {input_direction} is not valid, please select N or S.")
        
    return input_int, input_line, input_direction

def fetch_data_from_input(input_int: int) -> dict:
    """
    Collect input from the user to fetch real-time data for the selected subway line.

    Args:
        input_int: A number in the printed acceptable values, corresponding to a subway group string

    Returns:
        subway_data: A dict of MTA real-time data
    """
    subway_selector = mta_subway_fetcher.SUBWAY_SELECTOR_MAP[input_int-1]
    subway_data = mta_subway_fetcher.get_realtime_data(subway_selector)
    output_filepath = f'tmp/{subway_selector}.json'
    with open(output_filepath, 'w') as f:
        json.dump(subway_data, f, indent=2)
    return subway_data

def extract_subway_line(subway_line: str, subway_group_dict: dict) -> dict:
    """
    For a given group of subway lines, extract only the desired subway line.
    """
    line_stats = {'header': None, 'entity': []}
    line_stats['header'] = subway_group_dict['header']
    for e in subway_group_dict['entity']:
#        if (e.get('vehicle') and e['vehicle']['trip']['routeId'] == subway_line) or (e.get('tripUpdate') and e['tripUpdate']['trip']['routeId'] == subway_line): # Exlcuding the 'vehicle' message as it does not provide arrival times
        if e.get('tripUpdate') and e['tripUpdate'].get('stopTimeUpdate') and e['tripUpdate']['trip']['routeId'] == subway_line:
            line_stats['entity'].append(e)
    output_filepath = f'tmp/{subway_line}.json'
    with open(output_filepath, 'w') as f:
        json.dump(line_stats, f, indent=2)
    return line_stats

def find_next_arrival_times(subway_lines_stats: dict, station_name: str, direction: str, next_x_trains: int):
    """
    For a given subway line's data, a station stop, and a direction, find the next X arrival times.
    """
    full_station_name = station_name + direction
    inc = 0
    arrival_times = []
    for e in subway_lines_stats['entity']:
        if inc >= next_x_trains:
            break
        for i in e['tripUpdate']['stopTimeUpdate']:
            if i['stopId'] == full_station_name:
                arrival_times.append(i['arrival']['time'])
                inc += 1
    return arrival_times

def main():
    # input_int, preferred_subway, direction = get_subway_selection()
    input_int = 7; preferred_subway = "1"; direction = "S"; preferred_station = "127" # Example - downtown 1 train at Times Square
    
    subway_group_stats = fetch_data_from_input(input_int)
    subway_line_stats = extract_subway_line(preferred_subway, subway_group_stats)
    next_train_times = find_next_arrival_times(subway_line_stats, preferred_station, direction, 3)

    current_time = datetime.now().timestamp()
    for i in next_train_times:
        print(f"Train arriving in {int((int(i)-current_time) / 60.0)} minutes")

main()