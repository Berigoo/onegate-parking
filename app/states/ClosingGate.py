from app.core import SystemState, SessionQueue
from app.domain import EventType
from app.states import OpeningGate, HoldingGate

STATE_TIMEOUT = 5               # back to idle

class ClosingGate(SystemState): # sessions queue is empty, guaranteed
    def init(self):
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})
        self.context.gate_ctrl.close()
        self.context.sessions_queue = SessionQueue() # TODO proper cleaning
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_DETECTED:
                self.context.timer_mgr.stop()
                self.context.set_state("HoldingGate")
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.stop()
                self.context.set_state("OpeningGate")
            case EventType.GENERIC_TIMEOUT: # TODO proper close detection
                self.context.set_state("Idle")
            
        
        
