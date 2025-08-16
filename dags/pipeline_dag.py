from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from app.raw_loader import upload_raw_data_to_bronze
from app.silver_transform import process_bronze_to_silver
from app.gold_transform import process_silver_to_gold

import os


default_args = {
    'owner': 'admin',
    'retries': 5,
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
        task_id = "load-raw-to-bronze",
        python_callable = upload_raw_data_to_bronze
    )

    task_2 = PythonOperator(
        task_id = "process-bronze-to-silver",
        python_callable = process_bronze_to_silver
    )

    task_3 = PythonOperator(
        task_id = "process-silver-to-gold",
        python_callable = process_silver_to_gold
    )

    task_1 >> task_2 >> task_3
