# # # Currently unused function. # # #
import logging
from Tools.fileWriter import writeToJsonFile
from Tools.urlCleaner import parseOurDomainFromUrl

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def retHighRiskAppsDomainList(app_and_domain_name, app_risk_data) -> list:
    """
    Checks both list and returns a list of apps with high business risk.
    :param app_and_domain_name: List of dict os App names and URLs
    :param app_risk_data: List of dict of App names and Risk data
    :return: Destination list of High Risk Apps dest_list_of_highRisk_apps
    """

    dest_list_of_highRisk_apps = []
    listOfApp_data_to_write = []
    for appDomainData in app_and_domain_name:
        for appRiskDetail in app_risk_data:
            if appRiskDetail['businessRisk'] == 'high':
                if appRiskDetail['AppName'] == appDomainData['AppName']:
                    dest_list_of_highRisk_apps.append(parseOurDomainFromUrl(appDomainData['url']))
    if dest_list_of_highRisk_apps:
        listOfApp_data_to_write.append({
            'NumberOfHighRiskApps': len(dest_list_of_highRisk_apps),
            'destinationList': dest_list_of_highRisk_apps
        })
        writeToJsonFile(listOfApp_data_to_write, "destinationList")
        return dest_list_of_highRisk_apps
