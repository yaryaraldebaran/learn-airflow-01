from airflow.models import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

from datetime import datetime


DEFAULT_ARGS = dict(
    start_date=datetime(2021, 5, 5),
    owner="airflow",
    retries=0,
)

DAG_ARGS = dict(
    dag_id="multi_branch",
    schedule_interval=None,
    default_args=DEFAULT_ARGS,
    catchup=False,
)


def random_branch():
    from random import randint
    return "option_1" if randint(1, 2) == 1 else "option_2"


with DAG(**DAG_ARGS) as dag:
    t1 = DummyOperator(task_id="t1")

    t2 = BranchPythonOperator(task_id="t2", python_callable=random_branch)

    option_1 = DummyOperator(task_id="option_1")

    option_2 = DummyOperator(task_id="option_2")

    do_x = DummyOperator(task_id="do_x")

    do_y = DummyOperator(task_id="do_y")

    complete = DummyOperator(task_id="complete", trigger_rule=TriggerRule.NONE_FAILED)

    t1 >> t2 >> option_1 >> complete
    t1 >> t2 >> option_2 >> do_x >> do_y >> complete