"""
main file
"""

# things i need to do
# 1. Format a json for the playbooks nodes and vertices 
# 2. TODO: Create a function that update the json into a graph
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
    "id_1": []
  }
}
