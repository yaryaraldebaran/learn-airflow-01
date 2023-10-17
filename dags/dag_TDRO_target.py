from airflow.decorators import dag,task
from datetime import datetime


@dag(start_date=datetime(2023, 10, 16),schedule_interval='*/10 * * * *',catchup=False)
def target():
    @task
    def message(dag_run=None):
        print(dag_run.conf.get("message"))
    message()

target()