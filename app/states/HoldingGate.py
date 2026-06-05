from app.core import SystemState
from app.domain import EventType

STATE_TIMEOUT = 30

class HoldingGate(SystemState):
    def init(self):
        self.context.gate_ctrl.hold()
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})

    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.VEHICLE_GONE | EventType.GENERIC_TIMEOUT:
                self.context.timer_mgr.stop()
                self.context.set_state("ClosingGate")
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.stop()
                self.context.set_state("OpeningGate")
