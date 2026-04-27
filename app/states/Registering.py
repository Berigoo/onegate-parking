from app.core import SystemState
from app.domain import EventType, TextType

STATE_TIMEOUT=30                # back to IDLE

class Registering(SystemState):
    def init(self):
        self.session_id = self.context.current_event.payload["session_id"]
        
        self.context.timer_mgr.start(STATE_TIMEOUT * self.context.sessions_queue.qsize(), {"issuer": type(self).__name__})
    def execute(self):
        ev = self.context.current_event.type
        match ev:
            case EventType.CARD_IN_VALID:
                self.context.timer_mgr.stop()
                uid = self.context.current_event.payload["uid"]
                self.context.api_service.emit_uid(self.session_id, uid)
                self.context.set_context("Idle")
            case EventType.GENERIC_TIMEOUT:
                self.context.api_service.emit_uid(self.session_id, -1)
                self.context.set_context("Idle")
                
