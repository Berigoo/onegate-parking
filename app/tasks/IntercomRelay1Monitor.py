from bsp import bsp
import threading
import time
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType

class IntercomRelayMonitor:
    def __init__(self, queue_to_push: SessionQueue):
        self.queue = queue_to_push
        self.running = False
        self.thread = None
        self.logger = Logger("Intercom")
        self.last_state = False

    #################### threading methods
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    def _run(self):
        self.__setup()
        while self.running:
            self.__loop()
    ####################

    #################### Task Logic
    def __setup(self):
        # bsp.bsp_on_intercom_relay_high(self.__when_intercom_relay_high)
        pass
        
    def __loop(self):
        ret = bsp.bsp_read_intercom()
        print(ret is False)
        if self.last_state is False and ret is True:
            self.__when_intercom_relay_high()
            time.sleep(2)       # TODO proper debouncing
        self.last_state = ret

    def __when_intercom_relay_high(self):
        event = StateEvent(
            type=EventType.INTERCOM_OVERRIDE,
            payload=None
        )
        self.queue.put(event)
