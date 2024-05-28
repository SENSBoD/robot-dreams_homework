from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

# Constants
BUCKET_NAME = 'de-07-data-bucket'
GCS_FOLDER = '{{ ds }}/'
LOCAL_FILE_PATH = '/data/sales_{{ ds }}.csv'
DESTINATION_FILE_PATH = GCS_FOLDER + '{{ ds }}.csv'


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


dag = DAG(
    'upload_csv_to_gcs_bucket',
    default_args=default_args,
    description='Upload CSV files to GCS bucket',
    start_date=datetime(2022, 8, 9),
    # end_date=datetime(2022, 8, 10),
    # schedule_interval=timedelta(days=1),
    schedule_interval='@daily',
    catchup=False
)


for i in range(2):
    upload_task = LocalFilesystemToGCSOperator(
        task_id=f'upload_task_{i}',
        src=LOCAL_FILE_PATH,
        dst=GCS_FOLDER,
        bucket=BUCKET_NAME,
        dag=dag
    )