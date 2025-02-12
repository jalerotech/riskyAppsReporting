import logging
import re

from Tools.fileWriter import writeToJsonFile

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def parseOurDomainFromUrl(appURL):
    """
    Parses out the domain name from the app URL provided and created an entry for with
    destination list format
    :param appURL:
    :return:
    """
    dest_list_items = []
    for app in appURL:
        logger = logging.getLogger('riskyAppsReporting ')
        logger.info(f"Parsing out domain from url App URL -> {app['url']}")
        match = re.search(r'https?://([a-zA-Z0-9.-]+)', app['url'])
        if match:
            domain = match.group(1)
            data = {
                "destination": domain,
                "comment": f"Blocking {app['AppName']} App's url using automation"
            }
            dest_list_items.append(data)
    if dest_list_items:
        writeToJsonFile(dest_list_items, "destinationList")
        return dest_list_items
