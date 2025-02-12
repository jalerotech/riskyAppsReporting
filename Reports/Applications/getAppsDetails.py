import requests
import logging
from datetime import time
import time
from Auth.createAuth import get_access_token
from Tools.fileWriter import writeToJsonFile
from Tools.timeCheck import timeToRefresh
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb
from datetime import datetime, timezone

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
current_time_utc = datetime.now(timezone.utc)

token_creation_time = current_time_utc


def getAppsUrlName(list_of_app_data):
    """
    Produces a Lists applications url and name

    :param list_of_app_data: list of apps with their ids
    :return: list of app details related to app ID - []
    """
    handled = []
    logger = logging.getLogger('riskyAppsReporting: Running -> getAppsUrlName Script ')
    logger.info('Produce lists of discovered applications url and name..')
    url_and_appName_list = []
    listOfApp_data_to_write = []
    logger.info(f"Length of list of high risk app to process -> {len(list_of_app_data)}")
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id, rAb().api_key_secret)
    try:
        count = 0
        for appData in list_of_app_data:
            count += 1
            if timeToRefresh(expiry_time_stamp_unix):
                bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id,
                                                                                rAb().api_key_secret)
                logger.info(f"Fetching details for app id {appData['id']}, current count =>  ##{count}")
                header_to_use = rAb().headers
                header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
                app_details = retAppDetails(header_to_use, appData['id'])
                if app_details:
                    app_data = {
                        "AppName": app_details['name'],
                        'url': app_details['url']
                    }
                    url_and_appName_list.append(app_data)
                    handled.append(app_details['name'])
                    logger.info("Pausing for 2 seconds before making next request")
                    # # print(app_details)
                    # if app_details['category'] == "	Generative AI":
                    #     if app_details['weightedRisk'] == "high" or app_details['weightedRisk'] == "veryHigh":
                    #         print(app_details)
                    #         if app_details['name'] not in handled:
                    #             app_data = {
                    #                 "AppName": app_details['name'],
                    #                 'url': app_details['url'],
                    #                 'category': app_details['category'],
                    #                 'risk': app_details['weightedRisk']
                    #             }
                    #             url_and_appName_list.append(app_data)
                    #             handled.append(app_details['name'])
                    #             logger.info("Pausing for 2 seconds before making next request")
                time.sleep(2)
            else:
                logger.info(f"Fetching details for app id {appData['id']}, current count =>  ##{count}")
                header_to_use = rAb().headers
                header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
                app_details = retAppDetails(header_to_use, appData['id'])
                if app_details:
                    # if app_details['category'] == "	Generative AI":
                    #     if app_details['weightedRisk'] == "high" or app_details['weightedRisk'] == "veryHigh":
                    #         print(app_details)
                    #         if app_details['name'] not in handled:
                    #             app_data = {
                    #                 "AppName": app_details['name'],
                    #                 'url': app_details['url'],
                    #                 'category': app_details['category'],
                    #                 'risk': app_details['weightedRisk']
                    #             }
                    #             url_and_appName_list.append(app_data)
                    #             handled.append(app_details['name'])
                    app_data = {
                        "AppName": app_details['name'],
                        'url': app_details['url']
                    }
                    url_and_appName_list.append(app_data)
                    handled.append(app_details['name'])
                    logger.info("Pausing for 2 seconds before making next request")
                time.sleep(2)
        if url_and_appName_list:
            logger.info("Detailed list of APP created, returning list.")
            listOfApp_data_to_write.append({
                'DiscoveredAppsDetails': len(url_and_appName_list),
                'apps_name_url': url_and_appName_list
            })
            writeToJsonFile(listOfApp_data_to_write, "discoveredAppsDetails")
            return url_and_appName_list
    except Exception as e:
        logger.debug(f"retAppDetails returned None type object with error {e.args}")
        return None


def retAppDetails(header, appId):
    """
    Checks using a list of endpoint URLs for the details of discovered application.
    Produces the detail of the app (App ID) checked.
    :param appId: ID of the discovered application
    :param header: header from getAppsUrlName
    :return: App detail
    """
    logger = logging.getLogger('retAppDetails')
    logger.info('Fetching apps details using the APP ID.')
    try:
        for url in rAb().appDiscoveryUrlList:
            resp = requests.get(f"{url}/{appId}", headers=header)
            if resp.status_code == 200:
                logger.info("Got Successful response. Returning App Detail data.")
                return resp.json()
    except Exception as e:
        logger.debug(f"retAppDetails returned None type object with error {e.args}")
        return None

