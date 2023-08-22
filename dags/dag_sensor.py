from datetime import datetime, timedelta
from airflow import DAG 
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,8,20),
    'retries': 10,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='file_sensor_example',
    default_args=default_args,
    schedule_interval="5 * * * *",  # You can set this to a specific schedule if needed
    catchup=False,
)

wait_for_file = FileSensor( 
    task_id='wait_for_file', 
    filepath='../data/maang_stock_prices/AAPL.csv', 
    mode='poke', 
    timeout=300, 
    poke_interval=60,
    dag=dag
) 
wait_for_file