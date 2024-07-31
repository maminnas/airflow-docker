from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args={
    'owner':"airflow",
    'retries':'3',
    'retry_delay':timedelta(minutes=2),
}

with DAG(
    default_args=default_args,
    dag_id='dag_with_postgres_operator_v04',
    description="This dag is to try out Postgres connection",
    start_date=datetime(2024,7,30, 10),
    schedule_interval='0 0 * * *',
) as dag:
    table_name = 'dag_runs'
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        params={
            'database': 'postgres',
            'table_name': table_name,
        },
        sql="""
            CREATE TABLE IF NOT EXISTS {{ params.table_name }} (
                ds date,
                dag_id varchar,
                primary key (ds, dag_id)
            )
        """
    )

    task2 = PostgresOperator(
        task_id='insert_into_table',
        postgres_conn_id='postgres_localhost',
        # We can use JINJA templating to fetch variables
        # you can find those on airflow documentation webpage
        # https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#variables
        # params variable is set by us in the task(param={}) section for a way to pass the 
        # table name to the sql along with other jinja variables for airflow
        params={
            'database': 'postgres',
            'table_name': table_name,
        },
        sql="""
            INSERT INTO {{ params.table_name }} (ds, dag_id) VALUES( '{{ ds }}', '{{ dag.dag_id }}')
        """
    )

    task1 >> task2
