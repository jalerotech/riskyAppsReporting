from pathlib import Path
from dotenv import load_dotenv  # python-dotenv
import os
import json

env_path = Path('.') / 'authkey.env'
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    pass


class riskyAppsBlob:

    def __init__(self):
        # Content type for request headers
        self.contentType = 'application/json'

        # Loading AuthKeys via environment variables:

        self.api_key_id = os.getenv('api_key_id')
        self.api_key_secret = os.getenv('api_key_secret')

        # Auth and server URLs:

        self.AuthURL = "https://api.umbrella.com/auth/v2/token"
        self.server_base = "https://api.umbrella.com"

        # List Application URL

        # # General
        self.listApps = "https://api.umbrella.com/reports/v2/appDiscovery/applications"

        # US:
        self.listApps_US = "https://api.umbrella.com/reports.us/v2/appDiscovery/applications"

        # EUROPE:
        self.listApps_EMEA = "https://api.umbrella.com/reports.eu/v2/appDiscovery/applications"

        # Apps Discovery Url list:
        self.appDiscoveryUrlList = [self.listApps, self.listApps_US, self.listApps_EMEA]

        # Destination list

        self.DestListUrl = " https://api.umbrella.com/policies/v2/destinationlists"

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": ""
        }
