from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

DEFAULT_ARGS = {
    'depends_on_past': False,
    'email': ['admin@admin.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': 30,
}


def some_task_function():
    print('Hello from airflow!')

def some_task_function2():
    print('Hello from airflow!')

dag = DAG(
    dag_id='process_sales',
    start_date=datetime(2024, 4, 26),
    schedule_interval="0 1 * * *",
    catchup=False,
    default_args=DEFAULT_ARGS,
)

task1 = PythonOperator(
    task_id='extract_data_from_api',
    dag=dag,
    python_callable=some_task_function
)

task2 = PythonOperator(
    task_id='convert_to_avro',
    dag=dag,
    python_callable=some_task_function2
)


task1 >> task2