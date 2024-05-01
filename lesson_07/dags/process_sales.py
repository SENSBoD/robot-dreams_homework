from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import os
import requests


DEFAULT_ARGS = {
    'depends_on_past': False,
    'email': ['admin@admin.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': 30,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

JOB1_PORT = 8081
JOB2_PORT = 8082

RAW_DIR = os.path.join(BASE_DIR, "lesson_02", "raw", "sales", "2022-08-09")
STG_DIR = os.path.join(BASE_DIR, "lesson_02", "stg", "sales", "2022-08-09")


def run_job1():
    print("Starting job1:")
    resp = requests.post(
        url=f'http://localhost:{JOB1_PORT}/',
        json={
            "date": "2022-08-09",
            "raw_dir": RAW_DIR
        }
    )
    assert resp.status_code == 201
    print("job1 completed!")

def run_job2():
    print("Starting job2:")
    resp = requests.post(
        url=f'http://localhost:{JOB2_PORT}/',
        json={
            "raw_dir": RAW_DIR,
            "stg_dir": STG_DIR
        }
    )
    assert resp.status_code == 201
    print("job2 completed!")

dag = DAG(
    dag_id='process_sales',
    start_date=datetime(2022, 8, 9),
    end_date=datetime(2022, 8, 11),
    schedule_interval="0 1 * * *",
    catchup=True,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
)

task1 = PythonOperator(
    task_id='extract_data_from_api',
    dag=dag,
    python_callable=run_job1,
    trigger_rule=TriggerRule.ALL_SUCCESS
)

task2 = PythonOperator(
    task_id='convert_to_avro',
    dag=dag,
    python_callable=run_job2
)


task1 >> task2