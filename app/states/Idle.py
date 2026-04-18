from app.core import SystemState, DM
from app.domain import EventType, TextType

class Idle(SystemState):
    def init(self):
        DM.set_text(TextType.WELCOME)
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_TAP:
                self.context.set_state("SerialDataProcessing")
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state("OpeningGate")
            case EventType.VEHICLE_DETECTED:
                self.context.set_state("WaitingForEmoneyTap")
            case EventType.ASKING_FOR_SHUTDOWN:
                self.context.shutdown()
        
        
