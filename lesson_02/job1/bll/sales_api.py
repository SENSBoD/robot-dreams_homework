from lesson_02.job1.dal.sales_api import get_sales_from_api
import requests
import json
import os


# AUTH_TOKEN = os.environ['AUTH_TOKEN']
# API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app'


# Save json files to folder, named by date
def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    # TODO: implement me
    # 1. get data from the API
    # 2. save data to disk
    #
    # response = requests.get(
    #     url='https://fake-api-vycpfa6oca-uc.a.run.app',
    #     params={'date': date},
    # )

    clear_raw_directory(raw_dir)

    page = 1
    while True:
        response = get_sales_from_api(date, page)
        print(response)
        if response:
            file_name = f"sales_{date}_{page}.json"
            with open(os.path.join(raw_dir, file_name), "w") as f:
                json.dump(response, f, indent=4)
            page += 1
        else:
            break

# Clear the contents of the raw directory
def clear_raw_directory(raw_dir):
    if os.path.exists(raw_dir):
        for file in os.listdir(raw_dir):
            file_path = os.path.join(raw_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)