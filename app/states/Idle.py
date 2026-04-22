from app.core import SystemState
from app.domain import EventType, TextType

class Idle(SystemState):
    def init(self):
        self.context.dm.set_text(TextType.WELCOME)
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_TAP:
                self.context.set_state("SerialDataProcessing")
            case EventType.INTERCOM_OVERRIDE:
                self.context.set_state("AddingToQueue")
            case EventType.VEHICLE_DETECTED:
                self.context.set_state("WaitingForEmoneyTap")
            case EventType.ASKING_FOR_SHUTDOWN:
                self.context.shutdown()
        
        
