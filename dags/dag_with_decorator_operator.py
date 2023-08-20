from datetime import datetime, timedelta
from airflow.decorators import dag,task
from airflow.operators.python import PythonOperator

default_args={
    'owner':'ahyar',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
        dag_id='dag_with_taskflow_api_v5',
        default_args=default_args,
        start_date=datetime(2023,4,16),
        schedule_interval='@daily'
)
def hello_world_etl():
    @task(task_id="to_be_python_operator")
    def to_be_python_operator():
        print("this is python operator")
        return 
    @task(task_id="used_python_op")
    def used_python_op(value):
        print ("this is python operator 2")
        return 
    
    Ato_be_python_operator = PythonOperator(task_id="tobepythonoperator",python_callable=to_be_python_operator)
    Aused_python_op = PythonOperator(task_id="usedpythonop",python_callable=used_python_op)

    Ato_be_python_operator>>Aused_python_op

dag = hello_world_etl()