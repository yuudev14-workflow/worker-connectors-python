import importlib
module_name = "sample"

class Connector:
    def _read_config():
        pass

    def _get_module():
        module = importlib.import_module(f"src.connectors.{module_name}.connector")
        print(getattr(module, "z")(100))
        pass

# TODO: create a decorator that constantly read the configs and pass params from the function


# need to find a way to grab the connectors from the workflow, based on the connector name. 
# need to create a class for each connector that inherits from Connector and implements the required methods.
# we can execute the specifc action based on pyth getattr() function.
# need  to check if the function exists in the connector class before executing it.



# workflow in celery
