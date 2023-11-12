from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def _choose_best_model():
  #this method returns which task_id that should be executed after the branch
  accuracy = 6
  if accuracy > 5:
    return 'task_id_accurate'
  return 'task_id_inaccurate'

with DAG('branching', start_date=datetime(2023, 1, 1), schedule='@daily', catchup=False):
  choose_best_model = BranchPythonOperator(
    task_id='choose_best_model',
    python_callable=_choose_best_model
  )

  accurate = EmptyOperator(
    task_id='task_id_accurate'
  )

  inaccurate = EmptyOperator(
    task_id='tasi_id_inaccurate'
  )
  post_choice_final = EmptyOperator(
    task_id='post_choice_final'
  )
  post_choice_accurate = EmptyOperator(
    task_id="post_choice_accurate"
  )
  post_choice_inaccurate = EmptyOperator(
    task_id="post_choice_inaccurate"
  )

#   choose_best_model >> [accurate, inaccurate] >> post_choice_final
choose_best_model >> accurate >> post_choice_accurate >> post_choice_final
choose_best_model >> inaccurate >> post_choice_inaccurate >> post_choice_final
