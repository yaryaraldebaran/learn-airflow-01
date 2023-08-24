from airflow.decorators import dag,task
from datetime import datetime


@dag(start_date=datetime(2023,8,24),schedule='@daily',catchup=False)
def target():

    @task
    def message(dag_run=None):
        print(dag_run.conf.get("message"))

    message()

target()