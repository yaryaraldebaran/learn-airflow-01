from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'ahyar',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
def get_name(ti):
    ti.xcom_push(key='first_name',value='boim')
    ti.xcom_push(key='last_name',value='ald')

def greet(age,ti):
    first_name = ti.xcom_pull(task_ids='get_name',key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name',key='last_name')
    print(f"Hello, I am {first_name} and my last name {last_name}",f"I am {age} years old")

with DAG(
    dag_id='python_dag_v6',
    default_args=default_args,
    description='this is our first python dag',
    start_date=datetime(2023,4,16),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id = "greet",
        python_callable=greet,
        op_kwargs={'age':20}
    )
    task2=PythonOperator(
        task_id="get_name",
        python_callable=get_name
        # hasil return disimpan di pool xcom 
    )
    task2>>task1