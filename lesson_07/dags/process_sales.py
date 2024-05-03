from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
from airflow.providers.http.hooks.http import HttpHook


DEFAULT_ARGS = {
    'depends_on_past': False,
    'email': ['admin@admin.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': 30,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

RAW_DIR = os.path.join(BASE_DIR, "lesson_02", "raw", "sales", "2022-08-09")
STG_DIR = os.path.join(BASE_DIR, "lesson_02", "stg", "sales", "2022-08-09")


def run_job1():
    print("Starting job1:")
    hook = HttpHook(method='POST', http_conn_id='job1_connection')
    resp = hook.run(endpoint='',
                    json={
                        "date": "2022-08-09",
                        "raw_dir": RAW_DIR
                    })
    assert resp.status_code == 201
    print("job1 completed!")

def run_job2():
    print("Starting job2:")
    hook = HttpHook(method='POST', http_conn_id='job2_connection')
    resp = hook.run(endpoint='',
                    json={
                        "raw_dir": RAW_DIR,
                        "stg_dir": STG_DIR
                    })
    assert resp.status_code == 201
    print("job2 completed!")


with DAG('process_sales',
         start_date=datetime(2022, 8, 9),
         end_date=datetime(2022, 8, 11),
         schedule_interval="0 1 * * *",
         catchup=True,
         default_args=DEFAULT_ARGS,
         max_active_runs=1,
         ) as dag:
    task1 = PythonOperator(
        task_id='extract_data_from_api',
        python_callable=run_job1)
    task2 = PythonOperator(
        task_id='convert_to_avro',
        python_callable=run_job2
    )
    task1 >> task2