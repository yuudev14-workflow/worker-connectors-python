from celery import Celery
from collections import ChainMap

from src.logger.logging import logger

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
    if curr:
        result[curr] = True
    else:
        logger.warning("'curr' is not available in kwargs")
    
    
    return result
