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
        graph = {
            'START': ['A'],
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['E', 'D'],
            'D': [],
            'E': ['F'],
            'F': []
        }
        logger.debug(f"{graph=}")

        x = WorkflowGraph(graph=graph)
        x.generate_chain_task()