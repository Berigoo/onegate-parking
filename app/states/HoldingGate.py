from app.core import State
from app.domain import EventType
from app.states import OpeningGate, HoldingGate

class HoldingGate(State):
    def __init__(self):
        self.context.gate_ctrl.hold()        
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_GONE:
                self.context.set_state(ClosingGate())
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state(OpeningGate())
