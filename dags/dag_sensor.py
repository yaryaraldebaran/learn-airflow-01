from datetime import datetime, timedelta
from airflow import DAG 
from airflow.sensors.filesystem import FileSensor

dag_object = DAG(
    dag_id = "dag_sensor",
    start_date=datetime(2023,8,18),
    schedule_interval='@daily'
)

waiting_for_file = FileSensor(
    task_id='waiting_for_file',
    filepath='../notes.txt'
)

