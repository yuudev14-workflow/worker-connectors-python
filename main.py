"""
main file
"""



# things i need to do
# 1. Format a json for the playbooks nodes and vertices 
# 2. DONT DO: Create a function that update the json into a graph
# 3. Function that checks if graph is acyclical
# 4. Create a function for bfs
# 5. Connect to message queue
# 6. Traverse to the graph. Each Node in the graph will be a message send in message queue
# 7. TODO: Plan how to develop the connectors
# 8. TODO: Create a function that runs a connectors actions specified in the message queue


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import routes


def start_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

    )
    app.include_router(routes, prefix="/api")
    return app

app = start_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)