from app.core import State
from app.domain import EventType
from app.states import OpeningGate, HoldingGate

class ClosingGate(State):
    def __init__(self):
        self.context.gate_ctrl.close()        
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_DETECTED:
                self.context.set_state(HoldingGate())
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state(OpeningGate())
            
        
        
