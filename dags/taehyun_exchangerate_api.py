from datetime import datetime, timedelta
import requests
import json
import os 
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.slack_operator import SlackAPIPostOperator

default_args = {
    'owner': 'taehyun.jung',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 20),
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'taehyun_exchangerate_api',
    default_args=default_args,
    description='환율 정보 조회',
    schedule_interval=timedelta(days=1)
)

#### Functions ####
def call_exchangerate_api():
    url = 'https://api.apilayer.com/exchangerates_data/latest?symbols=USD,EUR&base=KRW'
    headers = {
        "apiKey": "your_api_key"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return data

def transform_json(**context):
    data = context['task_instance'].xcom_pull(task_ids='call_exchangerate_api')
    print(data)
    return data

def send_slack_message(**context):
    data = context['task_instance'].xcom_pull(task_ids='transform_json')
    message = f"환율 수집 완료:\n{data}"
    slack_token = 'your_slack_token'
    slack_channel = '#your_channel'
    slack_operator = SlackAPIPostOperator(
        task_id='send_slack_message_exchangerate',
        token=slack_token,
        channel=slack_channel,
        text=message,
        dag=dag
    )
    return slack_operator.execute(context=None)

#### DAGs ####
call_api = PythonOperator(
    task_id='call_exchangerate_api',
    python_callable=call_exchangerate_api,
    dag=dag
)

transform_json = PythonOperator(
    task_id='transform_json',
    python_callable=transform_json,
    provide_context=True,
    dag=dag
)

send_message = PythonOperator(
    task_id='send_slack_message',
    python_callable=send_slack_message,
    dag=dag
)

#### XCom ####
call_api >> transform_json >> send_message
