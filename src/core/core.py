"""
main file
"""

# things i need to do
# 1. Format a json for the playbooks nodes and vertices 
# 2. DONT DO: Create a function that update the json into a graph
# 3. TODO: Function that checks if graph is acyclical
# 4. TODO: Create a function for bfs
# 5. TODO: Connect to message queue
# 6. TODO: Traverse to the graph. Each Node in the graph will be a message send in message queue
# 7. TODO: Plan how to develop the connectors
# 8. TODO: Create a function that runs a connectors actions specified in the message queue

sample_json = {
    "name": "playbook_1",
    "description": "tests",
    "created_at": "tests",
    "created_by": "tests",
    "nodes": [
        {
            "id": "1shvkfsd",
            "description": "adasd"
        }
    ],

    "workflow": {
        "id_1": [] # list of ids its connected
    }
}



from collections import deque

def bfs(node: str, graph):
    visit = set()
    queue = deque()
    visit.add(node)
    queue.append(node)

    while queue:
        print(queue)
        for _ in range(len(queue)):
            curr = queue.popleft()
            for neighbor in graph[curr]:
                if neighbor not in visit:
                    visit.add(neighbor)
                    queue.append(neighbor)


def is_acyclic_graph(graph: dict):
    visit: set = set()
    stack: set = set()

    def dfs(node: str):
        if node in stack:
            return True
        
        if node in visit:
            return False
        
        visit.add(node)
        stack.add(node)


        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
            
        stack.remove(node)
        return False



    for node in graph:
        if dfs(node):
            return True
        
    return False


# check for acyclical graphs
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E', 'D'],
    'D': [],
    'E': ['F'],
    'F': []
}

print(is_acyclic_graph(graph))
bfs("A", graph)