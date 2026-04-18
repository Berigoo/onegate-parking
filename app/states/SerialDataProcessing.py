from app.core import SystemState
from app.domain import EventType

STATE_TIMEOUT = 15              # back to IDLE

class SerialDataProcessing(SystemState):
    def init(self):
        # TODO info message
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_IN_VALID | EventType.CARD_OUT_VALID:
                self.context.timer_mgr.stop()
                if self.context.current_event.payload["is_valid"]:
                    self.context.set_state("AddingToQueue")
                else:
                    # TODO info message, and maybe add sleep, so it can be rendered for n sec
                    self.context.logger.warning("Card invalid")
                    self.context.set_state("Idle")
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.stop()
                self.context.set_state("OpeningGate")
            case EventType.GENERIC_TIMEOUT:
                self.context.set_state("Idle")
            
        
        
