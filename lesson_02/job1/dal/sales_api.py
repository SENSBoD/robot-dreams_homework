from typing import List, Dict, Any
import requests
import json
import os


API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app'
AUTH_TOKEN = os.environ['AUTH_TOKEN']


# Get sales from API
def get_sales_from_api(date: str, page: int) -> Any | None:
    """
    Get data from sales API for specified date.

    :param date: data retrieve the data from
    :return: list of records
    """
    headers = {'Authorization': AUTH_TOKEN}
    response = requests.get(API_URL + f"/sales", params={'date': date, 'page': page}, headers=headers)
    if response.status_code == 200:
        sales_data = response.json()
        return sales_data
    else:
        print("Error fetching sales data:", response.text)
        return None

    # dummy return:
    # return [
    #     {
    #         "client": "Tara King",
    #         "purchase_date": "2022-08-09",
    #         "product": "Phone",
    #         "price": 1062
    #     },
    #     {
    #         "client": "Lauren Hawkins",
    #         "purchase_date": "2022-08-09",
    #         "product": "TV",
    #         "price": 1373
    #     },
    #     # ...
    # ]
