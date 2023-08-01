"""
Export all clients in DattoRMM to CSV DattoRMM via API

Returns:
    Create CSV file export_all.csv

SwaggerUI: https://syrah-api.centrastage.net/api/swagger-ui/index.html
"""

import csv
import os

import pandas as pd
from dotenv import load_dotenv

from dattormmapi import DattoRMMAPI

header = ["autotaskCompanyName", "person", "email"]
csv_file = "data/report_emails.csv"


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

    all_customers = pd.DataFrame()
    all_customers = dra.get_site_list(only_customers=True)
    sorted_customers = all_customers.sort_values(by=["autotaskCompanyName"], ignore_index=True)

    with open(csv_file, "w", newline="", encoding="UTF8") as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for index, customer in sorted_customers.iterrows():
            print(f"{customer['autotaskCompanyName']}")
            settings = dra.get_site_settings(customer["uid"])
            emails = ""
            all_recipients = settings["mailRecipients"]
            for recipient in all_recipients:
                if emails != "":
                    emails = emails + ";"
                emails = emails + recipient["email"]

            csv_row = [customer["autotaskCompanyName"], emails]
            writer.writerow(csv_row)


if __name__ == "__main__":
    main()
