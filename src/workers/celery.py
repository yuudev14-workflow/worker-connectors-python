from celery import Celery
from celery.signals import task_failure, task_prerun, task_success
from typing import Any
from kombu import Connection, Exchange, Queue
import json


from src.logger.logging import logger
from connectors.core.connector import Connector
from src.settings import settings

celery_app = Celery(
    "tasks", broker=settings.celery_broker, backend=settings.celery_backend
)


def send_task_status(workflow_history_id: str, task_id: str, status: str):
    # RabbitMQ connection parameters
    rabbit_url = settings.mq_url
    # Create a connection
    with Connection(rabbit_url) as conn:
        # Declare the queue
        queue = Queue(settings.workflow_processor_queue, durable=True)

        # Produce a message
        with conn.Producer() as producer:
            producer.publish(
                json.dumps(
                    {
                        "action": "task_status",
                        "workflow_history_id": workflow_history_id,
                        "task_id": task_id,
                        "status": status,
                    }
                ),
                exchange="",
                routing_key=queue.name,
                declare=[queue],
                delivery_mode=2,  # Make message persistent
            )


@celery_app.task
def task_graph(*args: tuple[dict] | dict | list[dict], **kwargs):
    # consolidate all the results from the tasks
    results = Connector.consolidate_results(*args)
    tasks_variables = {
        "steps": results,
    }
    curr: str = kwargs.get("curr", None)
    logger.info(f"executing {curr} in playbook.")
    task_information: dict = kwargs.get("task_information", {})
    workflow_history_id: dict = kwargs.get("workflow_history_id")

    if curr == "start":
        return results

    if curr not in task_information:
        raise Exception(f"operation ({curr}) does not exist in task_information")
    if curr is None:
        logger.warning("'curr' is not available in kwargs")
        return results

    operation_information: dict = task_information[curr]
    config_name = operation_information.get("config", None)
    parameters = operation_information.get("parameters", None)
    connector_name = operation_information.get("connector_name", None)
    operation = operation_information.get("operation", None)

    if connector_name is None:
        raise Exception(f"connector name is none for {curr}")

    try:

        send_task_status(
            workflow_history_id=workflow_history_id,
            task_id=operation_information.get("id"),
            status="in progress",
        )

        # get the class container
        connector = Connector.get_class_container(connector_name)

        # grab the config to use
        config = Connector.get_connector_config(
            config_name=config_name, connector_name=connector_name
        )

        params = Connector.evaluate_params(
            parameters=parameters, variables=tasks_variables
        )

        # execute the operations
        operation_result = connector.execute(
            configs=config, params=params, operation=operation
        )

        # assign the result for the operation
        logger.debug(f"execution complete for playbook, {operation=}")
        results[curr] = operation_result
        send_task_status(
            workflow_history_id=workflow_history_id,
            task_id=operation_information.get("id"),
            status="success",
        )

        return results
    except Exception as e:
        #  send log
        send_task_status(
            workflow_history_id=workflow_history_id,
            task_id=operation_information.get("id"),
            status="error",
        )
        raise e


# @task_prerun.connect(sender=task_graph)
# def task_prerun_handler(sender=None, **kwargs):
#     print("Pre-execution: Task is about to run")


# @task_success.connect(sender=task_graph)
# def task_success_handler(sender=None, **kwargs):
#     print("Task completed successfully")


# @task_failure.connect(sender=task_graph)
# def task_failure_handler(sender=None, **kwargs):
#     print("Task failed")
