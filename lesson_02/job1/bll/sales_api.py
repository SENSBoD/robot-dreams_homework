from lesson_02.job1.dal import local_disk, sales_api
import requests

import os
AUTH_TOKEN = os.environ['AUTH_TOKEN']

def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    # TODO: implement me
    # 1. get data from the API
    # 2. save data to disk
    #
    # response = requests.get(
    #     url='https://fake-api-vycpfa6oca-uc.a.run.app',
    #     params={'date': date},
    # )
    response = requests.get(
        url='https://fake-api-vycpfa6oca-uc.a.run.app/sales',
        params={'date': '2022-08-09', 'page': 2},
        headers={'Authorization': AUTH_TOKEN},
    )
    print("Response status code:", response.status_code)
    print("Response JSON", response.json())
    #

    print("\tI'm in get_sales(...) function!")
    pass
