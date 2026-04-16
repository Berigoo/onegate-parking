from app.core import State
from app.domain import EventType
from app.states import Idle, ClosingGate

STATE_TIMEOUT = 60              # back to IDLE

class WaitingForVehicleGone(State):
    def __init__(self):
        self.context.timer_mgr.start(STATE_TIMEOUT, self.__name__)
        self.next_low_signal = True
        self.current_vld_state = self.context.vld_monitor.get_state()

        if self.current_vld_state is True: # True = HIGH = Detected
            self.next_low_signal = False
        
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_DETECTED:
                self.next_low_signal = False
            case EventType.VEHICLE_UNDETECTED:
                if not self.next_low_signal:
                    self.context.timer_mgr.cancel()
                    self.context.set_state(ClosingGate())
            case EventType.GENERIC_TIMEOUT:
                self.context.set_state(ClosingGate())
            
        
        
