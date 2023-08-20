from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.bash import BashOperator

dag_object = DAG(
    dag_id = "simple_basic_bashoperator",
    start_date=datetime(2023,4,16),
    schedule_interval='@daily'
)

basic_bashOperator = BashOperator(
    task_id = "basic_bash",
    bash_command="echo 'Hello bash' ",
    dag=dag_object
)

basic_bashOperator