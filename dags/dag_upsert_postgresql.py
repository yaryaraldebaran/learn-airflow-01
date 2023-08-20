from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from util.util import input_sql_from_csv
import json

default_args = {"owner": "ahyar", "retries": 5, "retry_delay": timedelta(minutes=5)}

dag_object = DAG(
    dag_id = "upsert_postgresql",
    start_date=datetime(2023,8,20),
    schedule_interval='5 * * * *'
)


def upsert_to_postgres():
    # Retrieve the XCom values
    data_to_input = input_sql_from_csv()
    print(data_to_input)
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    for datas in data_to_input:
        sql_query = f"""INSERT INTO weather (city_name, temperature, description,windspeed) 
VALUES('{datas["city_name"]}', '{datas["temperature"]}','{datas["description"]}','{datas["windspeed"]}')
ON CONFLICT (city_name) 
do update set 
temperature= EXCLUDED.temperature,
description = EXCLUDED.description
;"""    
        hook.run(sql_query)
    

    
    

upsert_postgres_data=PythonOperator(
        task_id='upsert_to_postgres',
        python_callable=upsert_to_postgres,
        provide_context=True,
        dag=dag_object
    )

upsert_postgres_data