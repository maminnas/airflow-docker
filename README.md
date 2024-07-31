# Airflow Docker
This is a template on how to setup Airflow with docker
trying to add more to it as I learn along the way.
e.g. external executers, docker operators, kubernetes pods, AWS(MinIO), ML flows etc.
This project was done on July 24th, 2024 mostly following documentations of (Apache Airflow website)[https://airflow.apache.org/].

## Install Airflow
We can either install it using python and pip or install docker and use the official the airflow container (or can even make images from source files on git with our own changes added) (Link)[https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html]

We are focusing on dockerized version of airflow

## Install Docker
On laptop it's easy. Can add the documentation on how to do it on remote machines.

## Grab Airflow docker
(Link)[https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html] to Apache Airflow documentation for docker installation

example coming from (here)[https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html]
As mentioned in the documentation this example is not providing production level capabilities and is more for getting started.

Pull the docker compose
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml'
```

Set the environment
```
mkdir ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Initialize db:
```
docker compose up airflow-init
```

Running Airflow
```
docker compose up
```

Then in your DAG directory you can define your DAGs an it would be picked up by the shared volumes of containers. A DAG is defined as a python code.
It uses DAG module from airflow and we can define tasks and their order of dependancies.
After we save it the airflow webserver then should be able to pick this up and list it as one of the DAGs on the UI.

For now I just added a very simple example with two BashOperators coming one after the other.

## DAGs

We can define differente variety of tasks in a DAG. We start simple by adding Bash Operator and Python Operator. Then extend this with more complex and yet very commonly used task types e.g. S3 bucket, docker, kubernetes, run ML model etc.

## DAG Definition

1. Default: The sample file `myBashOperator.py` has a simple example. We instantiate a DAG with the needed arguments and then define each task according to our need. Finally, we specify the upstrea/downstream of the tasks and the order of execution for the DAG.

2. Task Flow API: In this variation we define our dag and their tasks using decorators @dag and @task and the dependency is inferred from this.

## XCOM

To pass values across tasks we can use XCOM. A task usually pushes it's return valye into XCOM but you can explicitly push results into XCOM if needed using `ti.xcom_push(key, value)` and pull the results from XCOM using `ti.xcom_pull(task_ids, key)`. You can find the example in `myPythonOperator.py`
