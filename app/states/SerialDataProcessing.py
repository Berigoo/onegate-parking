import os
import sqlite3
from app.core import SystemState
from app.domain import EventType

STATE_TIMEOUT = 15              # back to IDLE
ENTERED_USERS_DB = os.getenv('ENTERED_USERS_DB')

class SerialDataProcessing(SystemState):
    def init(self):
        # TODO info message
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})
        
    def execute(self):
        self.__check_or_create()
        ev = self.context.current_event.type
        
        match ev:
            case EventType.CARD_IN_VALID:
                self.context.timer_mgr.stop()
                if self.context.current_event.payload["is_valid"]:
                    uid = self.context.current_event.payload["uid"]
                    conn = sqlite3.connect(ENTERED_USERS_DB)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT 1 FROM entered_users WHERE uid=?",
                        (uid, )
                    )
                    row = cursor.fetchone()
                    conn.close()
                    
                    if row is not None:
                        self.context.set_state("Idle") # user already entered
                    else:
                        self.context.set_state("AddingToQueue")
                    
                else:
                    # TODO info message, and maybe add sleep, so it can be rendered for n sec
                    self.context.timer_mgr.stop()
                    self.context.logger.warning("Card invalid")
                    self.context.set_state("Idle")

            case EventType.CARD_OUT_VALID:
                self.context.timer_mgr.stop()
                if self.context.current_event.payload["is_valid"]:
                    self.context.timer_mgr.stop()
                    # do not care about "user already entered ?" info
                    self.context.set_state("AddingToQueue")
                else:
                    self.context.timer_mgr.stop()
                    # TODO info message, and maybe add sleep, so it can be rendered for n sec
                    self.context.logger.warning("Card invalid")
                    self.context.set_state("Idle")
            case EventType.INTERCOM_OVERRIDE:
                self.context.timer_mgr.stop()
                self.context.set_state("AddingToQueue")
            case EventType.GENERIC_TIMEOUT:
                self.context.set_state("Idle")
            
        def __check_or_create(self):
            conn = sqlite3.connect(ENTERED_USERS_DB)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entered_users (
                timestamp TIMESTAMP,
                uid TEXT,
                )
            """)

            conn.commit()
            conn.close()
            
