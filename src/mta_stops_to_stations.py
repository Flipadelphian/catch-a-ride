import src.mta_subway_fetcher as mta_subway_fetcher

def get_stops_for_lines(subway_lines: list[str]=mta_subway_fetcher.SUBWAY_LINE_LIST) -> dict:
    """
    Make API calls for real-time subway data to collect a list of stations per subway line, and return all available stations for the subway line(s).
    
    Args:
        subway_lines: A list of strings for the subway line(s) to search. Defaults to all possible subway lines.
    
    Returns:
        lines_with_stops: A dict of lists of strings, with keys as the names of subway lines and values as a list of machine-readable station IDs
    """
    lines_with_stops = {}
    for line in subway_lines:
        lines_with_stops[line] = []
        if line in mta_subway_fetcher.SHUTTLE_INTERNAL_MAPPING.keys():
            route_id = mta_subway_fetcher.SHUTTLE_INTERNAL_MAPPING[line]
        else: 
            route_id = line
        line_data = mta_subway_fetcher.get_realtime_data(line)['entity']
        for e in line_data:
            if e.get('vehicle') and e['vehicle']['trip']['routeId'] == route_id and e['vehicle'].get('stopId') and e['vehicle']['stopId'] not in lines_with_stops[line]:
                lines_with_stops[line].append(e['vehicle']['stopId'])
            elif e.get('tripUpdate') and e['tripUpdate']['trip']['routeId'] == route_id and e['tripUpdate'].get('stopTimeUpdate'):
                for stop in e['tripUpdate']['stopTimeUpdate']:
                    if stop['stopId'] not in lines_with_stops[line]:
                        lines_with_stops[line].append(stop['stopId'])
    return lines_with_stops

def remove_directionality_and_dedupe(lines_with_stops_both_directions) -> dict:
    """
    Take the output of function 'get_stops_for_lines' and remove all duplicate entries caused by direction included in station IDs.
    For example, 1 train station "66 St-Lincoln Center" has values ["124", "124N", "124S"] but should be reduced to "124"
    
    Args:
        lines_with_stops_both_directions: A dict of lists of strings, with keys as the names of subway lines and values as a list of machine-readable station IDs (possibly containing duplicate station IDs)
    
    Returns:
        new_lines_with_stops: A dict of lists of strings, with keys as the names of subway lines and values as a list of unique machine-readable station IDs
    """
    new_lines_with_stops = {}
    for line in lines_with_stops_both_directions.keys():
        new_lines_with_stops[line] = []
    for k,v in lines_with_stops_both_directions.items():
        for station in v:
            if station[-1] == "S" or station[-1] == "N":
                new_station = station[:-1]
            new_lines_with_stops[k].append(new_station)
        new_lines_with_stops[k] = list(set(new_lines_with_stops[k]))
    return new_lines_with_stops

def split_directionality_and_dedupe(lines_with_stops_both_directions) -> tuple[dict, dict]:
    """
    Take the output of function 'get_stops_for_lines', split into two dicts for each direction, and remove all duplicate entries included in station IDs.
    For example, 1 train station "66 St-Lincoln Center" has values ["124", "124N", "124S"]. If this were the only stop on the line, it would split into: {"1S": ["124S"]} and {"1N": ["124N"]}
    
    Args:
        lines_with_stops_both_directions: A dict of lists of strings, with keys as the names of subway lines and values as a list of machine-readable station IDs (possibly containing duplicate station IDs)
    
    Returns:
        lines_with_stops_north: A dict of lists of strings, with keys as the names of subway lines plus the "N" suffix and values as a list of unique machine-readable northbound station IDs
        lines_with_stops_south: A dict of lists of strings, with keys as the names of subway lines plus the "S" suffix and values as a list of unique machine-readable southbound station IDs
    """
    # Split dicts in half per line
    lines_with_stops_north = {}
    lines_with_stops_south = {}
    for line in lines_with_stops_both_directions.keys():
        lines_with_stops_north[f"{line}N"] = []
        lines_with_stops_south[f"{line}S"] = []

    # Extract north/south station IDs, discarding any non-directional IDs
    for k,v in lines_with_stops_both_directions.items():
        for station in v:
            if station[-1] == "N":
                lines_with_stops_north[f"{k}N"].append(station)
            elif station[-1] == "S":
                lines_with_stops_south[f"{k}S"].append(station)
    
    # Remove duplicates
    for line in lines_with_stops_both_directions.keys():
        lines_with_stops_north[f"{line}N"] = list(set(lines_with_stops_north[f"{line}N"]))
        lines_with_stops_south[f"{line}S"] = list(set(lines_with_stops_south[f"{line}S"]))
    
    return lines_with_stops_north, lines_with_stops_south