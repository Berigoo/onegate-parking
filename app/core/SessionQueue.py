from queue import Queue
from app.domain import StateEvent


class SessionQueue:
    """Session queue untuk menyimpan pengemudi yang mungkin mengatri"""

    def __init__(self):
        self._queue = Queue()

    def put(self, event: StateEvent):
        print(event)
        self._queue.put(event)

    def get(self, timeout=None):
        return self._queue.get(timeout=timeout)

    def empty(self):
        return self._queue.empty()

    def qsize(self):
        return self._queue.qsize()
