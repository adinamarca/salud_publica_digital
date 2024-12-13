"""Utility to get geodata from the Chilean Ministry of Environment API, using the requests library.
"""
import requests
from json import loads, dumps
from pathlib import Path
from time import sleep
from utils.db import insert

PATH_TO_SAVE_DATA = path = (Path(__file__).parent.parent/"data").joinpath("geodata.json")
PAGINATION_LIMIT = 100
BASE_URL = "https://arcgis.mma.gob.cl/server/rest/services/IDE/Cartografia_Base/FeatureServer/1/query"
URL = BASE_URL + "?where=1%3D1&outFields=*&f=json&resultOffset={start_from}&resultRecordCount={page_limit}"

data = []

def _get_geodata(url: str = URL, start_from: int = 0, page_limit: int = PAGINATION_LIMIT) -> dict:
    """Get geodata from the Chilean Ministry of Environment API.

    Args:
        url (str): The URL to the API endpoint.

        start_from (int): The starting index for the data.

        page_limit (int): The number of records to retrieve per request.

    Returns:
        dict: The geodata from the API
    """
    response = requests.get(url.format(start_from=start_from, page_limit=page_limit))
    data = response.content.decode("utf-8")
    return loads(data)

def get_all_geodata(url: str = URL, start_from: int = 0, page_limit: int = PAGINATION_LIMIT) -> list:
    """Get all geodata from the Chilean Ministry of Environment API.
    
    Args:
        url (str): The URL to the API endpoint.

        start_from (int): The starting index for the data.

        page_limit (int): The number of records to retrieve per request.
        
    Returns:
        dict: The geodata from the API
    """
    data = []
    while True:

        print(f"Getting geodata from {start_from} to {start_from + page_limit}")
        response = _get_geodata(url, start_from, page_limit)

        # Save the features from the response to the data list
        features = response.get("features", [])
        attributes = [feature.get("attributes") for feature in features]

        # Filter out the None values
        attributes = [attr for attr in attributes if attr]

        # Lower key names
        attributes = [{k.lower(): v for k, v in attr.items()} for attr in attributes]
        data.extend(attributes)
        start_from += page_limit

        # Throttle the requests to avoid exceeding API limits
        sleep(1)

        # Until the response has the exceededTransferLimit key set to False, the loop will continue
        if not response.get("exceededTransferLimit"):
            break
   
    return data

data = get_all_geodata()
insert("salud_publica_digital", "consultorio", data)