from celery import Celery
from celery.signals import task_failure, task_prerun, task_success


from src.logger.logging import logger
from connectors.core.connector import Connector
from src.settings import settings

celery_app = Celery(
    "tasks", broker=settings.celery_broker, backend=settings.celery_backend
)


@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict], **kwargs):
    # consolidate all the results from the tasks
    results = Connector.consolidate_results(*args)
    tasks_variables = {
        "steps": results,
    }
    curr: str = kwargs.get("curr")
    logger.info(f"executing {curr} in playbook.")
    task_information: dict = kwargs.get("task_information", {})
    if curr == "start":
        return results
    
    if curr not in task_information:
            raise Exception(
                f"operation ({curr}) does not exist in task_information"
            )
    if curr:
        operation_information: dict = task_information[curr]
        config_name = operation_information.get("config", None)
        parameters = operation_information.get("parameters", None)
        connector_name = operation_information.get("connector_name", None)
        operation = operation_information.get("operation", None)
        
        
        if connector_name is None:
            raise Exception(f"connector name is none for {curr}")

        # get the class container
        connector = Connector.get_class_container(connector_name)

        # grab the config to use
        config = Connector.get_connector_config(
            config_name=config_name, connector_name=connector_name
        )

        params = Connector.evaluate_params(parameters=parameters, variables=tasks_variables)

        # execute the operations
        operation_result = connector.execute(
            configs=config, params=params, operation=operation
        )

        # assign the result for the operation
        logger.debug(f"execution complete for playbook, {operation=}")
        results[curr] = operation_result
    else:
        logger.warning("'curr' is not available in kwargs")

    return results


# @task_prerun.connect(sender=task_graph)
# def task_prerun_handler(sender=None, **kwargs):
#     print("Pre-execution: Task is about to run")


# @task_success.connect(sender=task_graph)
# def task_success_handler(sender=None, **kwargs):
#     print("Task completed successfully")


# @task_failure.connect(sender=task_graph)
# def task_failure_handler(sender=None, **kwargs):
#     print("Task failed")
