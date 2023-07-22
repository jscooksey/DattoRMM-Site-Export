"""
Export all clients in DattoRMM to CSV DattoRMM via API

Returns:
    Create CSV file export_all.csv

SwaggerUI: https://syrah-api.centrastage.net/api/swagger-ui/index.html
"""

import os

import pandas as pd
from dotenv import load_dotenv

from dattormmapi import DattoRMMAPI


def main():
    """
    Main Function script
    """

    # Load URL and Keys from Environment variables
    load_dotenv()
    api_url = os.environ.get("API_URL")
    api_key = os.environ.get("API_KEY")
    api_secret_key = os.environ.get("API_SECRET_KEY")

    # Call dattormm_get_token function using defined parameters
    dra = DattoRMMAPI(api_url, api_key, api_secret_key)

    customers = dra.get_site_list(only_customers=True)
    customers.to_csv("export_all.csv", index=False)


if __name__ == "__main__":
    main()
