from app.core import State
from app.domain import EventType
from app.states import SerialDataProcessing, OpeningGate, WaitingForEmoneyTap

class Idle(State):
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_TAP:
                self.context.set_state(SerialDataProcessing())
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state(OpeningGate())
            case EventType.VEHICLE_DETECTED:
                self.context.set_state(WaitingForEmoneyTap())
            case EventType.ASKING_FOR_SHUTDOWN:
                self.context.shutdown()
        
        
