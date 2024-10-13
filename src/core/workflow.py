"""
workflow core file
"""

import celery
from celery import group, chain
from collections import deque
from collections.abc import Callable
from typing import Dict
from src.workers.celery import task_graph

class WorkflowGraph:
    """
    class responsible for generating chain tasks
    """
    def __init__(self, graph: Dict[str, list[str]], task_information):
        self.graph = graph
        self.task_information = task_information


    def generate_task(self, operation: str):
        """
        Generate a Celery task signature for a given value.

        This function creates a Celery task signature using the `task_graph` task and a dictionary
        containing the given value. The task signature is returned for further use in task chaining.

        Args:
            val (str): The value to be passed to the task.

        Returns:
            A Celery task signature for the given value.
        """
        return task_graph.s({
            operation: None,
        }, operation=operation, task_information=self.task_information)
    

    def generate_list_of_task(self, vals: list[str]):
        """
        Generate a list of Celery task signatures for a given list of values.

        This function creates a list of Celery task signatures using the `generate_task` method.
        If the input list contains only one value, a single task signature is returned.
        Otherwise, a Celery group of task signatures is returned.

        Args:
            vals (list[str]): A list of values to be passed to the tasks.

        Returns:
            celery.canvas.Group: A Celery group of task signatures for the given values.
            If the input list contains only one value, a single task signature is returned.
        """
        if len(vals) == 1:
            return self.generate_task(vals[0])
        return group(
            [self.generate_task(val) for val in vals]
        )


    def generate_chain_task(self):
        """
        Generates a chain of tasks based on the graph provided

        This function performs a breadth-first search (BFS) on the graph to generate a list of task

        The list of task signatures is then used to create a Celery chain using the `chain` function.

        Returns:
            A Celery chain of tasks based on the graph provided.
        """

        if self.is_acyclic_graph():
            raise Exception()
        
        task_chain_list = []

        self.bfs(lambda x: task_chain_list.append(self.generate_list_of_task(x)))
        
        task_chain = chain(*task_chain_list)
        return task_chain.apply_async()

    def bfs(self, callback: Callable, node: str = "START"):
        visit = set()
        queue = deque()
        visit.add(node)
        queue.append(node)

        while queue:
            callback(list(queue))
            for _ in range(len(queue)):
                curr = queue.popleft()
                for neighbor in self.graph[curr]:
                    if neighbor not in visit:
                        visit.add(neighbor)
                        queue.append(neighbor)


    def is_acyclic_graph(self):
        visit: set = set()
        stack: set = set()

        def dfs(node: str):
            if node in stack:
                return True
            
            if node in visit:
                return False
            
            visit.add(node)
            stack.add(node)


            for neighbor in self.graph[node]:
                if dfs(neighbor):
                    return True
                
            stack.remove(node)
            return False



        for node in self.graph:
            if dfs(node):
                return True
            
        return False

if __name__ == "__main__":
    task_information = {
        "START": {},
        "A": {
            "config": "sample",
        },
        "B": {
            "config": "sample",
        },
        "C": {
            "config": "sample",
        },
        "D": {
            "config": "sample",
        },
        "E": {
            "config": "sample",
        },
        "F": {
            "config": "sample",
        },
    }
    graph = {
        'START': ['A'],
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E', 'D'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    x = WorkflowGraph(graph=graph, task_information = task_information)