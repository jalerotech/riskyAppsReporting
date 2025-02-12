# # # Currently unused function. # # #
import requests
import logging
import time
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb
from Tools.timeCheck import timeToRefresh
from Auth.createAuth import get_access_token
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def getApplicationRisks(list_of_app_ids):
    """
    Produces a Lists applications and their associated risks, details using the app ID
    Note: The App URLs is not included in the risk report.
    the function getAppsUrlName returns data that has the url included.

    :param list_of_app_ids: list of apps with their ids
    :return: list of app details related to app ID - []
    """

    logger = logging.getLogger('riskyAppsReporting: Running -> getApplicationRisks Script ')
    logger.info('Produce lists of discovered applications risks...')
    listOfApp_w_risk_details = []
    handled = []
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id, rAb().api_key_secret)
    for appId in list_of_app_ids:
        if timeToRefresh(expiry_time_stamp_unix):
            bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id,
                                                                            rAb().api_key_secret)
            header_to_use = rAb().headers
            header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
            app_risk_data = retAppRiskDetails(header_to_use, appId)
            if app_risk_data:
                if app_risk_data['name'] not in handled:
                    app_data = {
                        "AppName": app_risk_data['name'],
                        "businessRisk": app_risk_data['businessRisk'],
                        "weightedRisk": app_risk_data['weightedRisk'],
                        'webReputation': app_risk_data['webReputation']
                    }
                    listOfApp_w_risk_details.append(app_data)
                    handled.append(app_risk_data['name'])
                logger.info("Pausing for 2 seconds before making next request")
                time.sleep(2)
        else:
            header_to_use = rAb().headers
            header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
            app_risk_data = retAppRiskDetails(header_to_use, appId)
            if app_risk_data:
                if app_risk_data['name'] not in handled:
                    app_data = {
                        "AppName": app_risk_data['name'],
                        "businessRisk": app_risk_data['businessRisk'],
                        "weightedRisk": app_risk_data['weightedRisk'],
                        'webReputation': app_risk_data['webReputation']
                    }
                    listOfApp_w_risk_details.append(app_data)
                    handled.append(app_risk_data['name'])
                logger.info("Pausing for 2 seconds before making next request")
                time.sleep(2)
    if listOfApp_w_risk_details:
        logger.info("Detailed list of APP Risks created, returning list.")
        return listOfApp_w_risk_details


def retAppRiskDetails(header, appId) -> dict:
    """
    Checks using a list of endpoint URLs for the risk details of discovered application.
    Produces the detail of the app (App ID) checked.
    :param appId: ID of the discovered application
    :param header: header from main class
    :return: App Risk detail
    """
    logger = logging.getLogger('retAppDetails')
    logger.info('Fetching apps details using the APP ID.')
    for url in rAb().appDiscoveryUrlList:
        resp = requests.get(f"{url}/{appId}/risk", headers=header)
        if resp.status_code == 200:
            logger.info("Got Successful response. Returning App Risk Detail data.")
            return resp.json()
