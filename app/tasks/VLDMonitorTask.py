from bsp import bsp
import threading
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType

class VLDMonitor:
    def __init__(self, queue_to_push: SessionQueue):
        self.queue = queue_to_push
        self.running = False
        self.thread = None
        self.logger = Logger("VLDMonitor")
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
    def get_state(self):
        return bsp.bsp_read_vld_in()

    def __setup(self):
        # bsp.bsp_on_vld_in_high(self.__when_vld_high)
        # bsp.bsp_on_vld_in_low(self.__when_vld_low)
        pass
        
    def __loop(self):
        ret = bsp.bsp_read_vld_in()
        if self.last_state is False and ret is True:
            self.__when_vld_high()
            sleep(2)            # TODO proper debouncing
        elif self.last_state is True and ret is False:
            self.__when_vld_low()
            sleep(2)
        self.last_state = ret

    def __when_vld_high(self):
        event = StateEvent(
            type=EventType.VEHICLE_DETECTED,
            payload=None
        )
        self.queue.put(event)

    def __when_vld_low(self):
        event = StateEvent(
            type=EventType.VEHICLE_GONE,
            payload=None
        )
        self.queue.put(event)
