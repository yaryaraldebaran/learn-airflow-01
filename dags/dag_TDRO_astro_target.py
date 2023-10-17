from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2023, 10, 16)
}

def _cleaning():
    print('Clearning from target DAG')
def _storing():
    print('Storing data from target DAG')

with DAG('target_dag_astro', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False) as dag:

    storing = PythonOperator(
        task_id='storing',
        python_callable=_storing
    )

    cleaning = PythonOperator(
        task_id='cleaning',
        python_callable=_cleaning
    )

    storing >> cleaning
