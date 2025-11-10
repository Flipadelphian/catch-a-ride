from src.gtfsproto import nyct_subway_pb2

import requests
from google.protobuf import json_format

SUBWAY_LINE_URL_SUFFIX = {
    'ACE_Sr': '-ace',
    'BDFM_Sf': '-bdfm',
    'G': '-g',
    'JZ': '-jz',
    'NQRW': '-nqrw',
    'L': '-l',
    '1234567_S': '',
    'SIR': '-si',
}

SUBWAY_SELECTOR_MAP = list(SUBWAY_LINE_URL_SUFFIX.keys())

SUBWAY_BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"

def api_to_bin(api_url: str) -> bytes:
    """
    Return the content of the API call in bytes, the format needed for protobuf-encoded data.

    Args:
        api_url: The API endpoint to collect real-time transit data
    
    Returns:
        r.content: The byte stream response from the API call
    """

    r = requests.get(url=api_url)
    return r.content

def bin_to_feedmessage(indata: bytes) -> dict:
    """
    Translate the protobuf-encoded data feed to a dict object.

    Args:
        indata: A stream of Protocol Buffer data collected from the MTA's real-time feed.

    Returns:
        message_dict: A dictionary output of the real-time feed, with expected format of:
            {
                'header': {dict_of_header_data}
                'entity': [list_of_dicts_of_transit_data]
            }
    """

    pb_data = nyct_subway_pb2.gtfs__realtime__pb2.FeedMessage() # Create an object for the incoming message feed type 
    pb_data.ParseFromString(indata) # Decode the input message
    message_dict = json_format.MessageToDict(pb_data) # Translate the message to a Python-readable dictionary
    return message_dict

def get_realtime_data(subway_line_group: str) -> dict:
    """
    Collect real-time subway data for the given line group.

    Args:
        subway_line_group: The identifier for the group of subway lines to be fetched. Must match one of the values in SUBWAY_SELECTOR_MAP.

    Returns:
        message_data: A dictionary of real-time subway details.
    """
    try:
        subway_realtime_api= f'{SUBWAY_BASE_URL}{SUBWAY_LINE_URL_SUFFIX[subway_line_group]}'
    except Exception as e:
        print(f"Error locating subway group: {e}")
        return None
    realtime_data = api_to_bin(subway_realtime_api)
    message_data = bin_to_feedmessage(realtime_data)
    return message_data
