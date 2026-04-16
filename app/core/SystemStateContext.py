from abc import ABC, abstractmethod
from app.domain import StateEvent
from app.core import Logger
import time
import sys

# the context class contains a _state that references the concrete state and setState method to change between states.
class SystemStateContext:

    def __init__(self, state: State, vld_monitor, card_validator_in, card_validator_out, intercom_relay, camera, gate_ctrl, timer_mgr) -> None:
        self.vld_monitor = vld_monitor
        self.card_validator_in = card_validator_in
        self.card_validator_out = card_validator_out
        self.intercom_relay = intercom_relay
        self.camera = camera
        self.gate_ctrl = gate_ctrl
        self.timer_mgr = timer_mgr
        self.logger = Logger("System State Context")
        self._state = None
        self.currrent_event: StateEvent = None
        
        self.setState(state)

    def set_state(self, state: State):
        self.logger(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def do(self, ev):
        self.current_event = ev
        self._state.execute()

    def shutdown(self):
        self.gate_ctrl.close()
        time.sleep(10)
        sys.exit(0)
