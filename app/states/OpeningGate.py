from app.core import State
from app.domain import EventType

class OpeningGate(State):
    def __init__(self):
        self.context.gate_ctrl.open()
        self.context.set_state(WaitingForVehicleGone())
        
    def execute(self):
        pass
