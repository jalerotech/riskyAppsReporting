from Reports.Applications.unApprovedApp import patchApplications
from urlsAndHeaders.urlsHeaderClass import riskyAppsBlob as rAb
from Reports.Applications.listAppsIDs import listHighVeryHighRiskApps
from Reports.Applications.getAppsDetails import getAppsUrlName
from Tools.urlCleaner import parseOurDomainFromUrl
from DestinationLists.createDestList import createDestinationList
from DestinationLists.addDomainsToDestList import addDestToDestList
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


def runMainProgram():
    """
    Runs main application.
    :return:
    """
    logger = logging.getLogger('riskyAppsReporting: ')
    logger.info('Running runMainProgram')
    try:
        listOfRiskyApps = listHighVeryHighRiskApps()
        if listOfRiskyApps:
            app_and_domain_name = getAppsUrlName(listOfRiskyApps)
            if app_and_domain_name:
                app_urls = parseOurDomainFromUrl(app_and_domain_name)
                dest_list_id = createDestinationList(rAb().DestListUrl)
                addDestToDestList(app_urls, dest_list_id, rAb().DestListUrl)
                patchApplications(listOfRiskyApps)
        else:
            logger.info(f'No high or veryHigh risk Generative AI Apps to process.')
    except TypeError as e:
        logger.info(f"An error occurred as while running functions that's part of the main program {e.args}")


if __name__ == '__main__':
    runMainProgram()
