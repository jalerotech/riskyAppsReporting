import json
import requests
from Auth.createAuth import get_access_token
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


def patchApplications(appList):
    """
    Added the notApproved label to high risk apps matching Gen Ai category.
    :param appList:
    :return:
    """
    logger = logging.getLogger('riskyAppsReporting ')
    bearer_token, org_id, expiry_time_stamp_unix = get_access_token(rAb().api_key_id,
                                                                    rAb().api_key_secret)
    header_to_use = rAb().headers
    header_to_use.update({'Authorization': f"Bearer {bearer_token}"})
    logger.info("Adding 'notApproved' label to high risk apps")
    if appList:
        appListToLabel = createListOfIds(appList)
        if appListToLabel:
            for url in rAb().appDiscoveryUrlList:
                payload_json = {"label": "notApproved",
                                "applicationsList": appListToLabel}
                payload_sting = json.dumps(payload_json)
                resp = requests.patch(url, headers=header_to_use, data=payload_sting)
                if resp.status_code == 200:
                    logger.info('High risk apps not approved.')
                    return


def createListOfIds(appList):
    list_of_app_ids = []
    target_labels = ["notApproved", "Approved"]
    for app in appList:
        if app['label'] not in target_labels:
            list_of_app_ids.append(app['id'])
    return list_of_app_ids
