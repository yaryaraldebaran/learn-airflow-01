from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from util.util import *

def get_csv_data():
    data_to_input = input_sql_from_csv("../data/maang_stock_prices/AAPL.csv")
    hook = PostgresHook(postgress_conn_id="postgres_localhost")
    for data in data_to_input:
        print(data)
        # sql_query = f"""INSERT INTO maang_table(name, date, open, high, low, close,adj_close,volume)
        # VALUES ('{data[""]}','{data['']}','{data['']}',{data['']},{data['']},{data['']},{data['']})"""

dag_object = DAG(
    dag_id="dag_maang_csv",
    start_date=datetime(2023,8,20),
    schedule_interval="5 * * * *" #setiap menit ke lima 
)
create_table_postgre = PostgresOperator(
    task_id = "create_postgres_table",
    postgres_conn_id="postgres_localhost",
    sql="""
create table if not exists maang_table(
id serial primary key,
name varchar(100) not null,
date date,
open float8,
high float8,
low float8,
close float8,
adj_close float8,
volume float8
)
""",
dag=dag_object
)
upsert_data=PythonOperator(
    task_id="upsert_to_postgres",
    python_callable=get_csv_data,
    provide_context=True,
    dag=dag_object
)


create_table_postgre >> upsert_data