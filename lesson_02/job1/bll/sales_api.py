from lesson_02.job1.dal.sales_api import get_sales_from_api
import json
import os


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    """
    Save json files to folder, named by date

    Args:
    - date: The date for which sales data is requested
    - raw_dir: Directory where sales data is saved

    Returns:
    - None
    """
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


def clear_raw_directory(raw_dir):
    """
    Clear raw directory
    """
    if os.path.exists(raw_dir):
        for file in os.listdir(raw_dir):
            file_path = os.path.join(raw_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)