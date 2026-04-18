from abc import ABC, abstractmethod
from app.domain import StateEvent
from app.core import Logger
from app.states import *
import time
import sys

# the context class contains a _state that references the concrete state and setState method to change between states.
class SystemStateContext:
    def __init__(self, state, vld_monitor, card_validator_in, card_validator_out, intercom_relay, camera, gate_ctrl, timer_mgr, sessions_queue) -> None:
        self.vld_monitor = vld_monitor
        self.card_validator_in = card_validator_in
        self.card_validator_out = card_validator_out
        self.intercom_relay = intercom_relay
        self.camera = camera
        self.gate_ctrl = gate_ctrl
        self.timer_mgr = timer_mgr
        self.sessions_queue = sessions_queue
        self.logger = Logger("System State Context")
        self.currrent_event: StateEvent = None

        self.set_state(state)

    def set_state(self, state):
        self.logger.debug(f"Context: Transitioning to {state}")
        self._state = STATE_MAP[state]() # TODO check
        self._state.context = self
        self._state.init()

    def do(self, ev):
        self.current_event = ev
        self._state.execute()

    def shutdown(self):
        self.gate_ctrl.close()
        time.sleep(10)
        sys.exit(0)
