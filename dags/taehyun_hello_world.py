from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import time

default_args = {
    'owner': 'taehyun.jung',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'taehyun_hello_world',
    default_args=default_args,
    description='처음 시작하는 Airflow',
    schedule_interval=timedelta(hours=1),
)

with dag:
    task_hello = BashOperator(
        task_id='task-hello',
        bash_command='echo "Hello"',
        dag=dag,
    )

    task_sleep = PythonOperator(
        task_id='sleep_task',
        python_callable=lambda: time.sleep(10),
        dag=dag,
    )

    task_world = BashOperator(
        task_id='task-world',
        bash_command='echo "World"',
        dag=dag,
    )

    task_hello >> task_sleep >> task_world