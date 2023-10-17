from airflow.decorators import dag,task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

@dag(start_date=datetime(2023, 10, 16), schedule_interval='*/5 * * * *', catchup=False)
def controller():

	@task
	def start():
		print("start")

	trigger = TriggerDagRunOperator(
		task_id='trigger_target_dag',
		trigger_dag_id='target',
		conf={"message": "this is from controller"},
		wait_for_completion=True
	)

	@task
	def done():
		print("done")

	start() >> trigger >> done()

controller()