from dataclasses import dataclass
from app.domain import EventType
import time

@dataclass
class StateEvent:
    type: EventType
    payload: dict
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
