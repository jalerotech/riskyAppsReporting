import json
import requests
from requests.auth import HTTPBasicAuth
import logging
import base64
from datetime import datetime, time, timezone

AuthURL = "https://api.umbrella.com/auth/v2/token"
server = "https://api.umbrella.com"

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


def get_access_token(api_key_id, api_key):
    """
    Creates the access token string using the API KEY ID and API KEY provided for a single org.

    :param api_key_id: API KEY ID
    :param api_key: API KEY
    :return: access_token str
    """
    logger = logging.getLogger('riskyAppsReporting: Running -> get_access_token Script ')
    logger.info('Generating Auth Token using API key.')

    auth_data = HTTPBasicAuth(api_key_id, api_key)
    resp = _retAuth(AuthURL, auth_data)
    try:
        access_token = resp["access_token"]
        validity = resp["expires_in"]
        org_from_access_token = access_token.split('.')[1]

        # Padding is required here to avoid getting incorrect padding error from the base64 decoding
        padded_org_from_access_token = f'{org_from_access_token}{"=="}'

        # Decoding the parsed data from base64 string to dict
        org_from_access_token_decoded = json.loads(base64.b64decode(padded_org_from_access_token).decode('utf-8'))
        org_id = org_from_access_token_decoded['sub'].split("/")[1]
        expiry_time_stamp_unix = org_from_access_token_decoded['exp']

        logger.info(f'Access Token created => {access_token}.')
        logger.info(f'Note that the token created is valid for {validity} seconds.')
        logger.info(f'The Access token is associated with your org ID => {org_id}')

        return access_token, org_id, expiry_time_stamp_unix

    except KeyError as e:
        logger.info(f"Error occurred as  -> {e.args}")

    # Additional data to present to the user about their org and potentially the rights associated with their API key.
    # parses out the part of the JWT containing the access token and then create a list by splitting


def _retAuth(authurl, auth_data):
    logger = logging.getLogger("_retAuth")
    try:
        re = requests.get(url=authurl, auth=auth_data, data=None)
        resp = re.json()
        return resp
    except Exception as e:
        logger.info(f"Request Failed with error -> {e.args}")


if __name__ == "__main__":
    key_id = ""
    key_secret = ""
    get_access_token(key_id, key_secret)
