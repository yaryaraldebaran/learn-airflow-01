from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from random import random

@dag(schedule_interval=None, start_date=days_ago(2), catchup=False)
def EXAMPLE_simple2():

    @task
    def task_1():
        # Generate a random number
        print("this is random")
        # return nothing
        return 
    
    @task
    def task_3():
        print("this is task 3")
        return

    @task
    def task_2(value1,value2):
        # Print the random number to the logs
        print(f'The randomly generated number is  .')

    # This will determine the direction of the tasks.
    # As you can see, task_2 runs after task_1 is done.
    # Task_2 then uses the result from task_1.
    task_2(task_1(),task_3())


dag = EXAMPLE_simple2()
