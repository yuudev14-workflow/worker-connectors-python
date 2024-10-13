from abc import ABC, abstractmethod
class Connector(ABC):

    @abstractmethod
    def execute(self, configs: dict, params: dict, operation: str, *args, **kwargs):
        raise NotImplementedError(f"execute function is not implemented in {self.__class__.__name__}")

    @abstractmethod 
    def health_check(self, configs: dict, params: dict, operation: str, *args, **kwargs):
        raise NotImplementedError(f"execute function is not implemented in {self.__class__.__name__}")
