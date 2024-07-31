from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args={
    'owner': 'airflow',
    'retries': 3,
    'retry_interval':timedelta(minutes=2)
}

@dag(dag_id='task_flow_v02',
     description='This is to test Task Flow',
     default_args=default_args,
     start_date=datetime(2024,7,29,2),
     schedule='@daily'
)
def hello_world_dag():
    
    @task(multiple_outputs=True)
    def get_name():
        return {'first_name':'Moin', 'last_name':'Amin'}
    
    @task()
    def get_age():
        return 30
    
    @task()
    def greet(first_name, last_name, age):
        print(f'Hello World! I am {first_name} {last_name} and I am {age} years old!')

    name = get_name()
    age = get_age()
    greet(name['first_name'], name['last_name'], age)

greet_dag = hello_world_dag()
