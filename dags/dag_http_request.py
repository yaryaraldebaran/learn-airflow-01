from datetime import datetime, timedelta
from airflow import DAG 
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import json


default_args={
    'owner':'ahyar',
    'retries' : 5,
    'retry_delay':timedelta(minutes=5)
}
def handle_response (response):
    if response.status_code==200:
        print("Received 200 OK")
        return True
    else:
        print("Error")
        return False
def process_response(response,ti):
    # Process the response here
    response_data = json.loads(response)
    city_name = response_data['name']
    description = response_data["weather"][0]["description"]
    temp = response_data["main"]["temp"]
    windspeed = response_data["wind"]["speed"]
    #create dict 
    dict_data = {
        "cityname":city_name,
        "description":description,
        "temp":temp,
        "windspeed":windspeed
    }
    #push to xcom 
    ti.xcom_push(key='dict_data',value=dict_data)    
def tes_xcomm(ti):
    print(ti.xcom_pull(task_ids="process_response"))

with DAG(
    dag_id='dag_with_http_request',
    default_args=default_args,
    start_date=datetime(2023,7,24),
    schedule_interval='0 0 * * *'
)as dag:
    http_request_task = SimpleHttpOperator(
        task_id='simple_http_request',
        method='GET',
        http_conn_id='http_connection',
        endpoint='data/2.5/weather',
        data={
            "lat":"-6.2",
            "lon":"106.882",
            "appId":"e353fdf2a125b862dad3a573ffadefbb"
        },
        response_check=lambda response: handle_response(response),
        dag=dag
    )
    process_response_task = PythonOperator(
        task_id='process_response',
        python_callable=process_response,
        op_args=[http_request_task.output],
        dag=dag
    )
    create_postgres_table = PostgresOperator(
        task_id="create_postgres_table",
        postgres_conn_id='postgres_localhost',
        sql="""
        create table if not exists weather(
            id SERIAL,
            city_name varchar(255),
            temp varchar(255),
            description varchar(255),
            windspeed varchar(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """   
    )
    tesxcomm=PythonOperator(
        task_id='testpull',
        python_callable=tes_xcomm,
        dag=dag
    )
    # insert_postgres_data=PostgresOperator(
    #     task_id = "insert_postgres_data",
    #     postgres_conn_id='postgres_localhost',
    #     sql="""
    #     INSERT INTO weather(city_name,temp,description,windspeed) VALUES (
    #         '{{ ti.xcom_pull(task_ids='process_response')['dict_data']['cityname'] }}', 
    #         '{{ ti.xcom_pull(task_ids='process_response')['dict_data']['description'] }}',
    #         '{{ ti.xcom_pull(task_ids='process_response')['dict_data']['temp'] }}',
    #         '{{ ti.xcom_pull(task_ids='process_response')['dict_data']['windspeed'] }}'
    #         );
    #     """,
    #     autocommit=True,
    #     )
    #create task that consume the xcom using PostgresOperator 
    #insert every key and value from the xcom dictionary
    http_request_task>>process_response_task>>create_postgres_table>>tesxcomm

# {
#     "coord": {
#         "lon": 106.882,
#         "lat": -6.2
#     }
# }