import sqlite3
import os
from datetime import datetime
from app.core import SystemState
from app.domain import EventType, TextType

ENTERED_USERS_DB = os.getenv('ENTERED_USERS_DB')bs

class CheckingForQueue(SystemState):
    def init(self):
        ev = self.context.sessions_queue.get() # guarantee CARD_IN_VALID or CARD_OUT_VALID or INTERCOM_OVERRIDE
        if ev.type is EventType.INTERCOM_OVERRIDE: # pass special access
            pass
        else:
        
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
