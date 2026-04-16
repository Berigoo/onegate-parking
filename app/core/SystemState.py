from abc import ABC, abstractmethod
from app.domain import EventType

class SystemState(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def execute(self) -> None:
        pass

