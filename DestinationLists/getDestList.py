from turtle import update
from typing import Tuple, Any

import requests
import logging
import json

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def fetchDestinationList(header, url):
    """
    Fetches list of the destination lists from the dashboard.

    :param url: Destination list API endpoint
    :param header: header from main class
    :return:
    """

    logger = logging.getLogger('fetchDestinationList: ')
    logger.info('Fetching list of destination lists.')

    resp = requests.get(url, headers=header, data=None)
    if resp.status_code == 200:
        if resp.json()['data']:
            # dest_list_id = [dest for dest in resp.json()['data'] if dest['name'] == "BlockHighRiskAppsDomains"]
            dest_list_id = next((dest for dest in resp.json()['data'] if dest['name'] == "BlockHighRiskAppsDomains"), None)

            # list_of_dest_lists = resp.json()['data']
            # for dest in list_of_dest_lists:
            #     if dest['name'] == "BlockHighRiskAppsDomains":
            #         print(dest['id'])
            # return dest_list_id[0]
            return dest_list_id


