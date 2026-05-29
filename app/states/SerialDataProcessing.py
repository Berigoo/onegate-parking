import os
import time
import sqlite3
from app.core import SystemState
from app.domain import EventType
import request

STATE_TIMEOUT = 15              # back to IDLE
ENTERED_USERS_DB = os.getenv('ENTERED_USERS_DB')

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")
API_BASE_URL = f"https://{SERVER_IP}:{SERVER_PORT}/api/active-entries"
TOKEN = os.getenv("SERVER_TOKEN_ACCESS")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

class SerialDataProcessing(SystemState):
    def init(self):
        # TODO info message
        self.context.timer_mgr.start(STATE_TIMEOUT, {"issuer": type(self).__name__})

    def __check_or_create(self):
        conn = sqlite3.connect(ENTERED_USERS_DB)
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS entered_users (
                timestamp TIMESTAMP,
                uid TEXT
                )
            """)

        conn.commit()
        conn.close()
            
    def execute(self):
        # self.__check_or_create()
        ev = self.context.current_event.type
        
        match ev:
            case EventType.CARD_IN_VALID:
                self.context.timer_mgr.stop()
                if self.context.current_event.payload["is_valid"]:
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/{uid}",
                            headers=headers,
                            timeout=5
                        )
                        # User already entered
                        if response.status_code == 200:
                            self.context.set_state("Idle")
                        # User not yet entered
                        elif response.status_code == 404:

                            response2 = requests.post(
                            f"{API_BASE_URL}",
                            headers=headers,
                            timeout=5
                        )
                            
                            if create_response.status_code in [200, 201]:
                                self.logger.debug(f"UID added: {uid}")
                                self.context.set_state("AddingToQueue")
                            else:
                                self.logger.error(
                                    f"Failed adding UID: "
                                    f"{create_response.status_code} "
                                    f"{create_response.text}"
                                )
                                self.context.set_state("Idle")
                        else:
                            self.logger.error(
                                f"Unexpected API status: {response.status_code}"
                            )
                            self.context.set_state("Idle")

                    except requests.RequestException as e:
                        self.logger.error(f"Laravel API request failed: {e}")
                        self.context.set_state("Idle")
                        
                else:
                    # TODO info message, and maybe add sleep, so it can be rendered for n sec
                    self.context.timer_mgr.stop()
                    self.context.dm.set_text("Kartu Invalid")
                    self.context.dm.set_color((0, 0, 255))
                    self.context.logger.warning("Card invalid")
                    time.sleep(3)
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
                self.context.timer_mgr.stop()
                self.context.set_state("Idle")

            # case EventType.CARD_OUT_TAP: # TODO rm
            #     self.context.set_state("AddingToQueue")
