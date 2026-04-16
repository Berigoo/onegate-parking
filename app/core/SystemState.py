from abc import ABC, abstractmethod
from app.domain import EventType

class SystemState(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def execute(self) -> None:
        pass

