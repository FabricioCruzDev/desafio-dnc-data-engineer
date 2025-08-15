from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from app.raw_loader import loader

import os


default_args = {
    'owner': 'admin',
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# Upload from raw to bronze
with DAG(
    dag_id = 'loader_dag',
    default_args = default_args,
    description = 'load raw data',
    start_date = datetime(2025, 1, 1),
    schedule_interval = '@daily',
    catchup = False
) as dag:
    
    task_1 = PythonOperator(
        task_id = "loader",
        python_callable = loader
    )

    task_1

# Clean data from bronze to silver

# Transform cleansed data from silver to gold