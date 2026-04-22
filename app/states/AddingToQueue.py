from app.core import SystemState
from app.domain import EventType, TextType

class AddingToQueue(SystemState):
    def init(self):
        self.context.sessions_queue.put(self.context.current_event) # guarantee CARD_IN_VALID or CARD_OUT_VALID or  INTERCOM_OVERRIDE
        self.context.set_state("OpeningGate")
    def execute(self):
        pass
