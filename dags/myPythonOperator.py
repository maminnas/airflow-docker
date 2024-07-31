from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner':'airflow',
    'retry': 3,
    'retry_interval':timedelta(minutes=2),
}


# def greet(name, age): # if we want to pass op_kwargs
def greet(ti): #ti stands for task instance (or task id?)
    # some errors to avoid
    # - xcom_pull not xcoms_pull
    # - task_ids not task_id
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'My name is {first_name} {last_name}, and I am {age} years old!')

def get_name(ti):
    ti.xcom_push(key='first_name', value='Moin')
    ti.xcom_push(key='last_name', value='Amin')
    # return 'Moin'

def get_age(ti):
    ti.xcom_push(key='age', value=30)

with DAG(
    default_args=default_args,
    dag_id='my_dag_with_python_operator_v06',
    description='This is a DAG using python operators.',
    start_date=datetime(2024, 7, 24, 2),
    schedule_interval='@daily',
    catchup=True, # default is also True
    # schedule_interval='0 2 */2 * *', # if we want we can use crontab schedules
) as dag:
    task1=PythonOperator(
        task_id='first_xcom_task',
        python_callable=greet,
        # op_kwargs={'name': 'Moin', 'age': 30},
    )
    
    task2=PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )

    task3=PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    [task2, task3] >> task1