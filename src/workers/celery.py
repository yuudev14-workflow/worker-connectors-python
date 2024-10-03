from celery import Celery, group, chain
import datetime

celery_app = Celery('tasks', broker='pyamqp://guest:guest@localhost:5672', backend='db+postgresql://postgres:password@localhost:5432/celery_logs?sslmode=disable', )

@celery_app.task
def task_a(x):
    print("Running task_a")
    return x + 1

@celery_app.task
def task_b(x):
    print("Running task_b")
    return x * 2

@celery_app.task
def task_c(x):
    print("Running task_c")
    return x - 3

@celery_app.task
def task_d(results):
    x, y = results  # Unpack the results from task_b and task_c
    print("Running task_d")
    return x + y

@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict]):
    from collections import ChainMap
    result = {}
    for arg in args:

        if isinstance(arg, dict):
            print("result ", arg)
            result = dict(ChainMap(result, arg))
        elif isinstance(arg, list) or isinstance(arg, tuple):
            print("result ", dict(ChainMap(*arg)))
            result = dict(ChainMap(*arg))
    return result

def create_dag(input_value):
    # Manually set task IDs
    custom_task_a_id = "custom_task_a_id"
    custom_task_b_id = "custom_task_b_id"
    custom_task_c_id = "custom_task_c_id"
    custom_task_d_id = "custom_task_d_id"

    # Create task chain with manually set task IDs
    task_chain = chain(
        task_a.s(input_value).set(task_id=custom_task_a_id),   # Manually set ID for Task A
        group(
            task_b.s().set(task_id=custom_task_b_id),          # Manually set ID for Task B
            task_c.s().set(task_id=custom_task_c_id)           # Manually set ID for Task C
        ),
        task_d.s().set(task_id=custom_task_d_id)               # Manually set ID for Task D
    )

    # Execute the chain
    result = task_chain.apply_async()

    return custom_task_a_id, custom_task_b_id, custom_task_c_id, custom_task_d_id