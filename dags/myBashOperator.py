from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args={
    'owner':"airflow",
    'retries':'3',
    'retry_delay':timedelta(minutes=2),
}

with DAG(
    default_args=default_args,
    dag_id='bash_dag',
    description="This is my first dag to try bash operators!",
    start_date=datetime(2024,7,22, 10),
    schedule_interval='@daily',
) as dag:
    task1 = BashOperator(
        task_id = "greet",
        bash_command="echo Hello World!"
    )

    task2 = BashOperator(
        task_id = "farewell",
        bash_command="echo Goodbye World!"
    )

    task1 >> task2