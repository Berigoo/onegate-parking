from app.core import SystemState
from app.domain import EventType, TextType
from app.states import SerialDataProcessing, Idle, OpeningGate

STATE_TIMEOUT = 30              # back to IDLE

class WaitingForEmoneyTap(SystemState):
    def init(self):
        self.context.dm.set_text(TextType.CARD_TAP_REQUEST)
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_TAP:
                self.context.timer_mgr.cancel()
                self.context.set_state("SerialDataProcessing")
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.cancel()
                self.context.set_state("OpeningGate")
            case EventType.GENERIC_TIMEOUT:
                self.context.set_state("Idle")
            
        
        
