from connectors.core.connector import Connector


class Sample(Connector):

    def execute(self, configs: dict, params: dict, operation: str, *args, **kwargs):
        print(f"executed, {operation}")
        return True
    
    def health_check(self, configs: dict, params: dict, operation: str, *args, **kwargs):
        print(f"executed, {operation}")
        return operation