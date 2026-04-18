from app.core import SystemState, DM
from app.domain import EventType, TextType

class AddingToQueue(SystemState):
    def init(self):
        self.context.sessions_queue.put(self.context.current_event) # guarantee CARD_IN_VALID or CARD_OUT_VALID
        self.context.set_state("OpeningGate")
    def execute(self):
        pass
