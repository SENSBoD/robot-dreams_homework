import os
import json
import fastavro

AUTH_TOKEN = os.environ['AUTH_TOKEN']
API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app'

def get_sales_from_api(date: str, page: int) -> dict:
    """
    Retrieve sales data from the API for a specific date and page.

    Args:
    - date (str): The date for which sales data is requested.
    - page (int): The page number of the sales data.

    Returns:
    - dict: Sales data retrieved from the API.
    """
    headers = {'Authorization': AUTH_TOKEN}
    response = requests.get(API_URL + f"/sales", params={'date': date, 'page': page}, headers=headers)
    if response.status_code == 200:
        sales_data = response.json()
        return sales_data
    else:
        print("Error fetching sales data:", response.text)
        return None

def save_sales_to_stg_dir(date: str, raw_dir: str, stg_dir: str) -> None:
    """
    Save sales data to the staging directory in Avro format.

    Args:
    - date (str): The date for which sales data is saved.
    - raw_dir (str): The directory path where the sales data is currently stored in JSON format.
    - stg_dir (str): The directory path where the sales data will be saved in Avro format.

    Returns:
    - None
    """
    page = 1
    while True:
        file_name = f"sales_{date}_{page}.json"
        raw_file_path = os.path.join(raw_dir, file_name)
        if os.path.exists(raw_file_path):
            with open(raw_file_path, "r") as f:
                sales_data = json.load(f)
                avro_file_name = f"sales_{date}_{page}.avro"
                avro_file_path = os.path.join(stg_dir, avro_file_name)
                with open(avro_file_path, "wb") as avro_file:
                    fastavro.writer(avro_file, sales_data, schema=None)
            page += 1
        else:
            break

if __name__ == '__main__':
    date = '2022-08-09'
    raw_dir = '/path/to/my_dir/raw/sales'
    stg_dir = '/path/to/my_dir/stg/sales'
    save_sales_to_stg_dir(date, raw_dir, stg_dir)
