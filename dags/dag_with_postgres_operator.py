from datetime import datetime, timedelta

from airflow import DAG 
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args ={
    'owner':'ahyar',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}
with DAG(
    dag_id='dag_with_postgres_operator_v1',
    default_args=default_args,
    start_date=datetime(2023,7,23),
    schedule_interval='0 0 * * *',
)as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
        create table if not exists dag_runs(
            dt date,
            dag_id character varying,
            primary key(dt, dag_id)
        )
        """   
    )
    task2 = PostgresOperator(
        task_id='insert_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
insert into dag_run (dt,dag_id) value ('{{ ds }}','{{dag_id}}')
        """   
    )
    task1