from celery import Celery, group, chain
import datetime
from collections import ChainMap

celery_app = Celery('tasks', broker='pyamqp://guest:guest@localhost:5672', backend='db+postgresql://postgres:password@localhost:5432/celery_logs?sslmode=disable', )

@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict], **kwargs):
    
    result = dict()
    for arg in args:
        if isinstance(arg, dict):
            result = dict(ChainMap(result, arg))
        elif isinstance(arg, list) or isinstance(arg, tuple):
            result= dict(ChainMap(*arg))
    curr = kwargs.get("curr")
    result[curr] = True
    
    return result
