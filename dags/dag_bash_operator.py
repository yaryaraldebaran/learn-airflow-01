from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'ahyar',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


with DAG(
    dag_id='our_first_dag_v4',
    default_args=default_args,
    description='this is our first dag',
    start_date=datetime(2023,4,16,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id = 'idtask1',
        bash_command='echo hello world this is the first task'
    )
    task2=BashOperator(
        task_id='idtask2',
        bash_command='echo this is second task'
    )
    task3= BashOperator(
        task_id='taskid3',
        bash_command='echo this is task 3 command'
    )

# task1.set_downstream(task2)
# task1.set_downstream(task3)

# task1 >> task2 
# task2 >> task3

task1 >> [task2,task3]