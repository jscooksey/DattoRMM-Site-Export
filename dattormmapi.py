"""
Class to interact with DattoRMM API    
"""

import pandas as pd
import requests
import validators


class DattoRMMAPI:
    """
    DattoRMM API class
    """

    def __init__(self, api_url: str, api_key: str, api_secret: str):
        """
        Initialise the class.  Get access token for remaiing method calls

        Args:
            api_url (str): URL to be used for all API call. ie https://syrah-api.centrastage.net
            api_key (str): API Key to be used for authentication
            api_secret (str): API Secret to be used for authentication
        """

        # Validate the passed variables
        if validators.url(api_url):
            self.api_url = api_url
        else:
            self.api_url = ""
            return
            # Abort object creaation
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = ""

        headers = {"ContentType": "application/x-www-form-urlencoded"}
        api_uri = f"{api_url}/auth/oauth/token"
        payload = {"grant_type": "password", "username": api_key, "password": api_secret}

        response = requests.post(url=api_uri, data=payload, headers=headers, auth=("public-client", "public"), timeout=5)

        tokens = response.json()
        self.token = tokens["access_token"]

    def __str__(self):
        return f"DattoRMM API URL = {self.api_url}"

    def get_site_list(self, only_customers: bool) -> pd.DataFrame:
        """
        Gets list of all sites in DattoRMM portal

        Args:
            only_customers (bool): True to only return customers and remove system Sites

        Returns:
            pd.DataFrame: Pandas DataFrame containing details of all sites
        """

        headers = {"Authorization": f"Bearer {self.token}", "ContentType": "application/json"}

        api_uri = f"{self.api_url}/api/v2/account/sites"
        response = requests.get(api_uri, headers=headers, timeout=5)
        results = response.json()

        # Import the first page of results in to Pandas DataFrame
        df_sites = pd.DataFrame(results["sites"])

        page_details = results["pageDetails"]

        # While we still have another page of results continue to that page
        # and concat results in to primary Pandas DataFrame
        while page_details["nextPageUrl"]:
            response = requests.get(page_details["nextPageUrl"], headers=headers, timeout=5)
            results = response.json()
            page_details = results["pageDetails"]
            df_sites = pd.concat([df_sites, pd.DataFrame(results["sites"])], ignore_index=True)

        # Convert the remaining devicesStatus column from JSON string to additional DataFrame columns
        df_devicesStatus = pd.json_normalize(df_sites.devicesStatus)
        df_sites = pd.concat([df_sites, df_devicesStatus], axis=1, sort=False)

        # Drop the rows of the DattoRMM System Sites if only_customers is true
        if only_customers:
            df_sites = df_sites[df_sites["name"].str.contains("Managed") == False]
            df_sites = df_sites[df_sites["name"].str.contains("OnDemand") == False]
            df_sites = df_sites[df_sites["name"].str.contains("Deleted Devices") == False]

        return df_sites

    def get_site_variables(self, site_uid: str):
        """
        Get all site variables for a particular site

        Args:
            site_uid (str): UID for the site requested

        Returns:
            _type_: Returns array of all site variables
        """
        headers = {"Authorization": f"Bearer {self.token}", "ContentType": "application/json"}

        api_uri = f"{self.api_url}/api/v2/site/{site_uid}/variables"
        response = requests.get(api_uri, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"Failed Request {response.status_code}")
        data = response.json()

        return data["variables"]

    def update_site_variable(self, site_uid: str, var_id: int, value: str):
        """
        Update a site variable

        Args:
            site_uid (str): UID of the site in question
            var_id (int): Variable ID thats to be updated
            value (str): New value for the variable

        Returns:
            int: Request reposnse status
        """
        headers = {"Authorization": f"Bearer {self.token}", "ContentType": "application/json"}

        api_request_body = {"name": "strInstall", "value": value, "masked": False}

        api_uri = f"{self.api_url}/api/v2/site/{site_uid}/variable/{var_id}"
        response = requests.post(api_uri, headers=headers, json=api_request_body, timeout=5)

        if response.status_code != 200:
            print(f"Failed to update site varibale: {response.status_code}")

        return response.status_code

    def new_site_variable(self, site_uid: str, name: str, value: str):
        """
        Create a new site variable

        Args:
            site_uid (str): UID of the site to adjust
            name (str): Name of the variable
            value (str): Value of the variable

        Returns:
            int: Response code value
        """
        headers = {"Authorization": f"Bearer {self.token}", "ContentType": "application/json"}

        api_request_body = {"name": name, "value": value, "masked": False}

        api_uri = f"{self.api_url}/api/v2/site/{site_uid}/variable"
        response = requests.put(api_uri, headers=headers, json=api_request_body, timeout=5)

        if response.status_code != 200:
            print(f"Failed to create new site variable: {response.status_code}")

        return response.status_code
