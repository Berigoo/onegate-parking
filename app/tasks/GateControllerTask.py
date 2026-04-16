from bsp import bsp
from enum import Enum
import threading
from app.core import SessionQueue, Logger
from app.domain import StateEvent, EventType

class GateState(Enum):
    GATE_OPENING = "gate_opening"
    GATE_CLOSING = "gate_closing"

class GateController:
    def __init__(self):
        # self.running = False
        # self.thread = None
        self.logger = Logger("Gate Controller")
        self.is_holding  = False
        self.state: GateState = GateState.GATE_CLOSING

    #################### threading methods
    # def start(self):
    #     if self.running:
    #         return
    #     self.running = True
    #     self.thread = threading.Thread(target=self._run, daemon=True)
    #     self.thread.start()
    # def stop(self):
    #     self.running = False
    #     if self.thread:
    #         self.thread.join(timeout=5)
    # def _run(self):
    #     self.__setup()
    #     while self.running:
    #         self.__loop()
    ####################

    #################### Task Logic
    def open(self):
        bsp.bsp_write_boom_gate(True)
        self.state = GateState.GATE_OPENING
        self.logger.debug("opening the gate")
    def close(self):
        bsp.bsp_write_boom_gate(False)
        self.state = GateState.GATE_CLOSING
        self.logger.debug("closing the gate")
    def hold(self):
        bsp.bsp_write_boom_gate_hold()
        self.is_holding = True
        self.logger.debug("holding the gate")
    def continue(self):
        bsp.bsp_write_boom_gate(False)
        if self.is_holding and self.state is GateState.GATE_OPENING:
            self.open()
            self.is_holding = False
            self.state = GateState.GATE_OPENING
        else is self.is_holding and self.state is GateState.GATE_CLOSING:
            self.close()
            self.is_holding = False
            self.state = GateState.GATE_CLOSING
        self.logger.debug("continuing")
        
    def __setup(self):
        pass

    def __loop(self):
        pass
