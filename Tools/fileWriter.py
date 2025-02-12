import json
import logging

data_list = []
logger = logging.getLogger('File Writer')


def writeToJsonFile(data_to_write, label) -> None:
    """
    Writes data to json files
    :param label: discovered_apps, highRiskAppsData, destinationList
    :param data_to_write: data to write to file
    :return: None
    """
    if label == "discoveredAppsIds":
        logger.info(f"writeToJsonFile: Writing data {data_to_write} to the discoveredAppsIds.json file")
        file_name = 'Files/discoveredAppsIds.json'
        _writeToFile(data_to_write, file_name)

    if label == "discoveredAppsDetails":
        logger.info(f"writeToJsonFile: Writing data {data_to_write} to the discoveredAppsDetails.json file")
        file_name = 'Files/discoveredAppsDetails.json'
        _writeToFile(data_to_write, file_name)

    if label == "destinationList":
        logger.info(f"writeToJsonFile: Writing data {data_to_write} to the HighRiskAppDestList.json file")
        file_name = 'Files/HighRiskAppDestList.json'
        _writeToFile(data_to_write, file_name)


def _writeToFile(data, file_name):
    # Cleans up the file before writing to it.
    with open(file_name, 'w') as json_file:
        logger.info(f"{file_name} opened")
        logger.info(f'Cleaning up {file_name} file')
        json_file.close()
        logger.info(f'{file_name} file cleaned \n ')

    #  Writes the entry_data one line at a time in the reminder_data.json file. No list needed here -> Evaluating the best performance in the reminder feature.
    with open(file_name, 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')
