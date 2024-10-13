from fastapi import APIRouter, HTTPException
from src.core.workflow import WorkflowGraph
from src.logger.logging import logger
import logging


router = APIRouter()


class CeleryController:
    def __init__(self):
        pass

    @router.get("/celery")
    async def celery_workflow():
        task_information = {
            "START": {},
            "A": {
                "config": "sample",
                "connector_name": "sample",
            },
            "B": {
                "config": "sample",
                "connector_name": "sample",
            },
            "C": {
                "config": "sample",
                "connector_name": "sample",
            },
            "D": {
                "config": "sample",
                "connector_name": "sample",
            },
            "E": {
                "config": "sample",
                "connector_name": "sample",
            },
            "F": {
                "config": "sample",
                "connector_name": "sample",
            },
        }
        graph = {
            "START": ["A"],
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["E", "D"],
            "D": [],
            "E": ["F"],
            "F": [],
        }
        logger.debug(f"{graph=}")

        x = WorkflowGraph(graph=graph, task_information=task_information)
        x.generate_chain_task()
