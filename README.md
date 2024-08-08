# Airflow Docker
This is a template on how to setup Airflow with docker
trying to add more to it as I learn along the way.
e.g. external executers, docker operators, kubernetes pods, AWS(MinIO), ML flows etc.
This project was done on July 24th, 2024 mostly following documentations of [Apache Airflow website](https://airflow.apache.org/).

## Install Airflow
We can either install it using python and pip or install docker and use the official the airflow container (or can even make images from source files on git with our own changes added) [Link](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

We are focusing on dockerized version of airflow

## Install Docker
On laptop it's easy. Can add the documentation on how to do it on remote machines.

## Grab Airflow docker
[Link](https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html) to Apache Airflow documentation for docker installation

example coming from [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
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

## TaskFlow API

In this variation we define our DAGs using `airflow.decorators` specifically `@dag` and `@task` and let it infere the dependancy. You can find the sample code in `taskFlow.py`. To pass the returned values into XCOM, if they need to return more than one value you should specify `multiple_outputs=True` in the `@task` section.

# Postgres Connector

One of the main use cases of Airflow is for ETL and that certainly requires connection to databases. Here we try out a connection with our postgres that is running on docker for out airflow. We update our `docker-compose.yaml` to expose the postgres port and make it accessible to other connectors.

The first step is to define a connection on airflow web page. We go to Admin -> Connections. From there we set a name for the connection_id, type of connection, and required information for connection e.g. host, schema, user, pass, port, access_key, etc. The id is used in DAG codes to be used with the appropriate Operators (in this case with PostgresOperator). To connecnt to a docker hosted postgres we use `host.docker.internal` instead of `localhost`.
Checkout the code in `myPostgresOperator.py` for more details on the usage of the `postgresOperator`.
In the code you can see that `{{ Jinja templating }}` is used in the sql query to access some runtime variables or pass some parameters.

# Sensor
This is a special operator that waits for something to occure. This is great when we don't know the exact time when the file exists. For this case we use **MinIO** which is going to mimic an S3 for us in a container.

## MinIO

Reading from [MinIO documentation](https://min.io/docs/minio/container/index.html) here is how we can run it locally in container:
```
https://min.io/docs/minio/container/index.html
```

First off we add minio service to out docker-compose. After successfully running it on docker we go the `http://localhost:9001` to access the WebUI of MinIO. With credentials specified in docker compose we login and create a bucket named `airflow-raw-data` and upload a sample `data.csv` file.

## Create Connection

To connect to S3 or MinIO we need to define the S3 connection on Airflow admin page and we can anme it `minio_s3_conn`. For this we need these info:
```
{
    "aws_access_keys_id":"<YOUR_ACCESS__KEY>",
    "aws_secret_access_key:"<YOUR_SECRET_KEY>",
    "endpoint_url": "http://host.docker.internal:9000"
}
```


## Airflow Package: Providers.amazon

In the airflow.providers we should have amazon packages. To check this we can `docker exec -it <airflow-webserver-ID> bash` to get into the docker container. Then we can `pip list | grep amazon` to see if this already exists and what version is installed. At the time I was running this here was my output:

```
apache-airflow-providers-amazon          8.25.0
```

Knowing this we can go to [Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.25.0/_api/airflow/providers/amazon/index.html) for more precise explanation on [usage of S3 Sensor](https://airflow.apache.org/docs/apache-airflow-providers-amazon/8.25.0/operators/s3/s3.html).

If the package we want is not installed we can use a requirements.txt and a Dockerfile and extend the image we are using to have our packages. This is especially helpful on ML tasks as well when there are very specific ML related packages needed. I will have that on a later section.

## Sensor operator

The S3KeySensor Operator is used to poke the file_name that we are looking for in a bucket and when it finds it it finishes successfully. This can be a trigger to our DAG. THere are many options to use for this to match with regex, wildcard, fetch list of previous results fetched, etc. 

A simple case can be found in `mySensorOperator.py`. We are only looking for the key (file name) `data.csv`. We are poking it every 5 seconds and it tries it for 60 seconds before results in fail.

There is also anotehr sensor Operator on S3 named `S3KeysUnchangedSensor` to check for changes in the number of objects at a specific prefix in an Amazon S3 bucket and waits until the inactivity period has passed with no increase in the number of objects. This can be a good indicator that a task that was keep adding new files to a path is now completed and we can start doing our next task.
