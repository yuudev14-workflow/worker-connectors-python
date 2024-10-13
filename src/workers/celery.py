from celery import Celery
from celery.signals import task_failure, task_prerun, task_success
from collections import ChainMap
import importlib
import inspect
import tomllib

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

def get_connector_config(config_name: str, connector_name: str):
    if config_name is not None:
        with open(f"./connectors/{connector_name}/configs/{config_name}.toml", "rb") as f:
            return tomllib.load(f)
    return {}


@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict], **kwargs):
    # consolidate all the results from the tasks
    results = consolidate_results(*args)
    operation: str = kwargs.get("operation")
    task_information: dict = kwargs.get("task_information", {})
    if operation == "START":
        return results
    if operation:
        if operation not in task_information:
            raise Exception(f"operation ({operation}) does not exist in task_information")
        operation_information: dict = task_information[operation]
        config_name = operation_information.get("config", None)
        connector_name = operation_information.get("connector_name", None)
        if connector_name is None:
            raise Exception(f"connector name is none for {operation}")

        # get the class container
        connector = get_class_container(connector_name)

        # grab the config to use
        config = get_connector_config(config_name=config_name, connector_name=connector_name)
        

        # execute the operations
        operation_result = connector.execute(configs=config, params={}, operation=operation)

        # assign the result for the operation
        results[operation] = operation_result
    else:
        logger.warning("'curr' is not available in kwargs")
    
    return results


@task_prerun.connect(sender=task_graph)
def task_prerun_handler(sender=None, **kwargs):
    print("Pre-execution: Task is about to run")

@task_success.connect(sender=task_graph)
def task_success_handler(sender=None, **kwargs):
    print("Task completed successfully")

@task_failure.connect(sender=task_graph)
def task_failure_handler(sender=None, **kwargs):
    print("Task failed")