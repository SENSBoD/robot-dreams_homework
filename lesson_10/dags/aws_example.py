from airflow import DAG
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from datetime import datetime
from airflow.operators.dummy import DummyOperator

BUCKET_NAME = 'my-data-bucket-super-latest'
AWS_FOLDER = '{{ ds }}/'
LOCAL_FILE_PATH = '/data/sales_clean.csv'
DESTINATION_FILE_PATH = AWS_FOLDER + '{{ ds }}.csv'

# DAG definition
with DAG(
        'upload_local_to_s3_dag',
        default_args={
            'owner': 'airflow',
            'start_date': datetime(2023, 5, 1),
        },
        description='DAG to upload a local file to S3 using a specific operator',
        schedule_interval=None,
        catchup=False,
        tags=['example'],
) as dag:
    start_task = DummyOperator(
        task_id='start'
    )

    # Create a task to upload a file to S3
    upload_file_to_s3 = LocalFilesystemToS3Operator(
        task_id='upload_local_file_to_s3',
        filename=LOCAL_FILE_PATH,  # Path to the local file
        dest_key=DESTINATION_FILE_PATH,  # The destination path in S3
        dest_bucket=BUCKET_NAME,  # S3 bucket name
        replace=True,  # Set to True to overwrite existing files
        aws_conn_id='aws_default',  # AWS connection ID
    )
    end_task = DummyOperator(
        task_id='end'
    )

    start_task >> upload_file_to_s3 >> end_task
