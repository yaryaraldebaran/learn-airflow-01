from airflow.decorators import dag, task
from airflow import Dataset
from datetime import datetime

data_a = Dataset("s3://bucket_a/data_a")
data_b = Dataset("s3://bucket_b/data_b")

@dag(start_date=datetime(2023,8,24),schedule='@daily',catchup=False)
def producer():
    @task(outlets=[data_a])
    def update_a ():
        print("update A")
    
    @task(outlets=[data_b])
    def update_b ():
        print("update B")

    update_a() >> update_b()

producer()