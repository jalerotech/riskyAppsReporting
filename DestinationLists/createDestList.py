import requests
import logging
import json

from Auth.createAuth import get_access_token
from DestinationLists.getDestList import fetchDestinationList
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def createDestinationList(url) -> int:
    """
    Create blocking destination list and returns the list id.

    :param url: Destination list API endpoint
    :return: int
    """
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id,
                                                                    rAb().api_key_secret)
    header_to_use = rAb().headers
    header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
    logger = logging.getLogger('riskyAppsReporting: ')
    logger.info('Running -> createDestinationList')

    payload = {
        "access": "block",
        "isGlobal": False,
        "name": "BlockHighRiskAppsDomains",
        "bundleTypeId": 1
    }
    resp = requests.post(url, headers=header_to_use, data=json.dumps(payload))
    if resp.status_code == 200:
        try:
            if resp.json()['statusCode']:
                if resp.json()['statusCode'] == 409:
                    logger.info("Destination list named 'BlockHighRiskAppsDomains' already exists, fetching its ID.")
                    return fetchDestinationList(header_to_use, url)['id']
        except KeyError as e:
            logger.debug(f"'statusCode key not present in resp.json(), meaning that the DL is not yet present on the dashboard, as error {e.args} suggests.'")
            logger.info("No existing DL named 'BlockHighRiskAppsDomains', a new one had been created.")
            logger.info(f"Destination list container created with id -> {resp.json()['data']['id']}.")
            return resp.json()['data']['id']


