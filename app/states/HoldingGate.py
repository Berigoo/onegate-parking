from app.core import SystemState
from app.domain import EventType
from app.states import OpeningGate, HoldingGate

class HoldingGate(SystemState):
    def init(self):
        self.context.gate_ctrl.hold()        
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_GONE:
                self.context.set_state("ClosingGate")
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state("AddingToQueue")
