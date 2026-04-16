from app.core import SystemState
from app.domain import EventType

class OpeningGate(SystemState):
    def init(self):
        self.context.gate_ctrl.open()
        self.context.set_state("WaitingForVehicleGone")
        
    def execute(self):
        pass
