from app.core import State
from app.domain import EventType
from app.states import Idle, OpeningGate

STATE_TIMEOUT = 15              # back to IDLE

class SerialDataProcessing(State):
    def __init__(self):
        self.context.timer_mgr.start(STATE_TIMEOUT, self.__name__)
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_IN_VALID | EventType.CARD_OUT_VALID:
                self.context.timer_mgr.cancel()
                self.context.set_state(OpeningGate())
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.cancel()
                self.context.set_state(OpeningGate())
            case EventType.GENERIC_TIMEOUT:
                self.context.set_state(Idle())
            
        
        
