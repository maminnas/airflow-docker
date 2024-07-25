Juky 24th, 2024
This is a template on how to setup Airflow with docker
trying to add more to it as I learn along the way.
e.g. external executers, docker oeprators, kubernetese pods, aws(MinIO), ML flows etc.

# Install Airflow
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

Then in your DAG directory you can define a dag. a dag is defined as a python code.
It used DAG module from airflow and we can define tasks and their order and save it.
The airflow webserver then should be able to pick this up and list it as one of the dags.

For now I just added a very simple example with two BashOperators coming one after the other.
