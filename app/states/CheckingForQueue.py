import sqlite3
from datetime import datetime
from app.core import SystemState, DM
from app.domain import EventType, TextType

ENTERED_USERS_DB = "entered_users.db"

class CheckingForQueue(SystemState):
    def init(self):
        ev = self.context.sessions_queue.get() # guarantee CARD_IN_VALID or CARD_OUT_VALID
        uid = ev.payload["uid"]

        conn = sqlite3.connect(ENTERED_USERS_DB)
        cursor = conn.cursor()
        if ev.type is EventType.CARD_IN_VALID:
            cursor.execute(
                "INSERT INTO entered_users (timestamp, uid) VALUES(?, ?)",
                (datetime.now(), uid)
            )
        else:
            cursor.execute(
                "DELETE FROM entered_users WHERE uid=?",
                (uid,)
            )
        conn.commit()
        conn.close()

        if self.context.sessions_queue.empty():
            self.context.set_state("ClosingGate")
            return

        self.context.set_state("WaitingForVehicleGone")
        
    def execute(self):
        pass
