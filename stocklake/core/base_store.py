from abc import ABC, abstractmethod


class BaseStore(ABC):
    @abstractmethod
    def save(self, *args, **kwargs):
        pass
