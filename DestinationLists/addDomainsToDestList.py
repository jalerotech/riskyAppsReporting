import requests
import logging
import json

from Auth.createAuth import get_access_token
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def addDestToDestList(list_of_appdomains, dest_list_id, url):
    """
    Adds the list of high risk domains to the created destination list container
    :param list_of_appdomains: formatted destination lists with comments
    :param dest_list_id: ID of destination list
    :param url: Destination list updating url
    :return: None
    """
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id,
                                                                    rAb().api_key_secret)
    header_to_use = rAb().headers
    header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
    logger = logging.getLogger('addDestToDestList: ')
    logger.info('Running -> addDestToDestList')
    if dest_list_id:
        resp = requests.post(f"{url}/{dest_list_id}/destinations", headers=header_to_use, data=json.dumps(list_of_appdomains))
        if resp.status_code == 200:
            logger.info(f"Destinations added to destination list {dest_list_id}")
    else:
        logger.info("No destination list id provided so exiting program...")


