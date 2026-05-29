from app.core import SystemState
from app.domain import EventType, TextType

class AddingToQueue(SystemState):
    def init(self):
        self.context.sessions_queue.put(self.context.current_event) # guarantee CARD_IN_VALID or CARD_OUT_VALID or  INTERCOM_OVERRIDE. tmp: CARD_OUT_TAP
        
        # tmp
        # if self.context.current_event.type is EventType.CARD_OUT_TAP:
        #     self.context.set_state("OpeningGate")
        #     return
        if self.context.current_event.type is EventType.INTERCOM_OVERRIDE:
            self.context.set_state("OpeningGate")
            return
        
        name = self.context.current_event.payload["name"]
        if name is None:
            self.context.dm.set_text("Selamat Datang")
        else:
            self.context.dm.set_text("Selamat Datang " + name)
        self.context.set_state("OpeningGate")
    def execute(self):
        pass
