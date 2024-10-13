from celery import Celery
from collections import ChainMap
import importlib
import inspect

from src.logger.logging import logger
from connectors.core.connector import Connector
from src.settings import settings

celery_app = Celery('tasks', broker=settings.celery_broker, backend=settings.celery_backend)

def consolidate_results(*args: tuple[dict] | dict | list[dict]) -> dict:
    """
    This consolidates all the results
    
    Args:
        args (tuple[dict] | dict | list[dict]) = all results in the tasks

    Returns:
        consolidated results
    """
    results = dict()
    for arg in args:
        if isinstance(arg, dict):
            results = dict(ChainMap(results, arg))
        elif isinstance(arg, list) or isinstance(arg, tuple):
            results= dict(ChainMap(*arg))
    return results

def get_class_container(connector_name: str):
    module: Connector = importlib.import_module(f"connectors.{connector_name}.connector")
    connector_classes = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Connector) and obj != Connector:
            connector_classes.append(obj)

    if len(connector_classes) > 1:
        logger.warning(f"found {len(connector_classes)} classes that inherits from Connector. Choosing the first class integrated")
    
    connector: Connector = connector_classes[0]()
    return connector



@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict], **kwargs):
    # consolidate all the results from the tasks
    results = consolidate_results(*args)
    curr = kwargs.get("curr")
    if curr:
        # get the class container
        connector = get_class_container(curr)

        # execute the operations
        operation_result = connector.execute({},{}, curr)

        # assign the result for the operation
        results[curr] = operation_result
    else:
        logger.warning("'curr' is not available in kwargs")
    
    return results
