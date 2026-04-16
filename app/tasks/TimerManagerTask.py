import time
import threading
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType

class TimerManager:
    def __init__(self, queue_to_push: SessionQueue):
        self.running = False
        self.thread = None
        self.logger = Logger("Timer Manager")
        self.timer = None
        self.queue = queue_to_push
        self.payload = None
        
    #################### threading methods
    def start(self, timeout, payload):
        self.stop()
        self.timer = threading.Timer(self.timeout, self._timeout)
        self.running = True
        self.payload = payload
        self.timer.start()
    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
    def _timeout(self):
        event = StateEvent(
            type=EventType.GENERIC_TIMEOUT,
            payload=self.payload
        )
        self.queue.put(event)
        
    ####################

    #################### Task Logic
    def reset(self):
        self.start()
