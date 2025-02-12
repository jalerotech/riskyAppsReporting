import requests
import logging

from Auth.createAuth import get_access_token
from Tools.fileWriter import writeToJsonFile
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

listOfAllDiscoveredApp_ids = []
generalListOfApp_data = []
listOfApp_data_to_write = []
riskyGenAIApps = []


def listHighVeryHighRiskApps():
    """
    Produces a Lists discovered applications with high and veryHigh weighted risks
    :return:
    """
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id, rAb().api_key_secret)
    logger = logging.getLogger('riskyAppsReporting: Running -> listHighVeryHighRiskApps Script ')
    logger.info('Produce lists of high risk discovered applications...')
    # Update the header the with bearer token
    header = rAb().headers
    header.update({'Authorization': f"Bearer {bearer_token}"})

    try:
        # Initial offset values used as results paging.
        offset_values = [0, 100]
        for offset_val in offset_values:
            listOfApps = retListOfApp(header, offset_val)
            if listOfApps:
                if offset_val >= 100:
                    offset_val += 100
                    offset_values.append(offset_val)
                    logger.info(f'offset used {offset_val}')
                    createLists(listOfApps)
                else:
                    logger.info(f'Not using offset.')
                    createLists(listOfApps)
        if riskyGenAIApps:
            logger.info("List of APP IDs created, returning list.")
            listOfApp_data_to_write.append({
                'TotalHigh-VeryHigh_Risk_GenAI_Apps': len(riskyGenAIApps),
                'apps': riskyGenAIApps
            })
            writeToJsonFile(listOfApp_data_to_write, "discoveredAppsIds")
            return riskyGenAIApps  # # to return in customer environment
        else:
            return generalListOfApp_data  # # to return in test/lab environment
    except Exception as e:
        logger.debug(f"An error occurred while running listHighVeryHighRiskApps module. {e.args}")


def retListOfApp(header, offset_val):
    """
    Checks using a list of endpoint URLs for the discovered applications for a particular customer.
    Produces a raw list of Apps.
    :param offset_val: offset value
    :param header: header from main class
    :return: List of Apps
    """
    logger = logging.getLogger('retListOfApp')
    logger.info('Checking apps using a list of endpoint URLs.')
    for url in rAb().appDiscoveryUrlList:
        query_parameter = {
            "limit": 100,
            "offset": offset_val
        }
        resp = requests.get(url, headers=header, params=query_parameter)
        if resp.status_code == 200:
            logger.info("Got Successful response. Returning collected data.")
            if len(resp.json()['items']) != 0:
                logger.info(f"Current returned batch of discovered apps => batch size: {len(resp.json()['items'])}, batch: {resp.json()['items']}")
                return resp.json()['items']
            else:
                logger.info(f"empty json/list file returned {resp.json()['items']} so app id fetch completed.")
                return None


def createLists(listOfApps):
    target_labels = ["notApproved", "Approved"]
    target_weightedRisks = ["high", "veryHigh"]
    for app in listOfApps:
        if app['id'] not in listOfAllDiscoveredApp_ids:
            listOfAllDiscoveredApp_ids.append(app['id'])
            # Filtering further for generative ai apps
            if app['category'] == "Generative AI":
                if app['weightedRisk'] in target_weightedRisks:
                    if app['label'] not in target_labels:
                        riskyGenAIApps.append({
                            'id': app['id'],
                            'name': app['name'],
                            'label': app['label'],
                            'risk': app['weightedRisk']
                        })
            # else:
            #     if app['label'] != "notApproved":
            #         app_data = {
            #             'id': app['id'],
            #             'name': app['name'],
            #             'label': app['label'],
            #             'risk': app['weightedRisk']
            #         }
            #         generalListOfApp_data.append(app_data)
