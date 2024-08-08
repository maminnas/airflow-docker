from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args={
    'owner': 'airflow',
    'retries':3,
    'retry_delay':timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_minio_s3_v02',
    default_args=default_args,
    start_date=datetime(2024,8,7),
    schedule_interval='@daily',
) as dag:
    task1=S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow-raw-data',
        bucket_key='data.csv',
        aws_conn_id='minio_s3_conn',
        mode='poke',
        poke_interval=5,
        timeout=60
    )

    task1