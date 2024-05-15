from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.dummy import DummyOperator

# Constants
BUCKET_NAME = 'de-07-data-bucket'
GCS_FOLDER = '{{ ds }}/'
LOCAL_FILE_PATH = '/data/sales_clean.csv'
DESTINATION_FILE_PATH = GCS_FOLDER + '{{ ds }}.csv'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
        'gcs_upload_example',
        default_args=default_args,
        description='A simple DAG to upload files to GCS',
        schedule_interval=None,
        start_date=datetime(2024, 5, 14),
        catchup=False,
        tags=['example'],
) as dag:
    start_task = DummyOperator(
        task_id='start'
    )

    # Task to upload a file to GCS
    upload_file_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_file_to_gcs',
        src=LOCAL_FILE_PATH,
        dst=DESTINATION_FILE_PATH,
        bucket=BUCKET_NAME,
        mime_type='text/plain'
    )

    end_task = DummyOperator(
        task_id='end'
    )

    start_task >> upload_file_to_gcs >> end_task
