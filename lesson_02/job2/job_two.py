import os
import json
import requests
import fastavro
from schema import schema


AUTH_TOKEN = os.environ['AUTH_TOKEN']
API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app'


def save_sales_to_stg_dir(raw_dir: str, stg_dir: str) -> None:
    """
    Save sales data to the staging directory in Avro format.

    Args:
    - date (str): The date for which sales data is saved.
    - raw_dir (str): The directory path where the sales data is currently stored in JSON format.
    - stg_dir (str): The directory path where the sales data will be saved in Avro format.

    Returns:
    - None
    """
    date = os.path.basename(os.path.normpath(raw_dir))

    page = 1
    while True:
        file_name = f"sales_{date}_{page}.json"
        raw_file_path = os.path.join(raw_dir, file_name)
        if os.path.exists(raw_file_path):
            with open(raw_file_path, "r") as f:
                sales_data = json.load(f)
                avro_file_name = f"sales_{date}_{page}.avro"
                avro_file_path = os.path.join(stg_dir, avro_file_name)
                print(avro_file_path)

                with open(avro_file_path, "wb") as avro_file:
                    fastavro.writer(avro_file, schema, sales_data)
            page += 1
        else:
            break