import sqlite3
import os
from datetime import datetime
from app.core import SystemState
from app.domain import EventType, TextType
import requests

API_BASE_URL = "http://localhost:8000/api/active-entries"
TOKEN = "1|BROFIjULCvHGKq1pn1h7i0V4Z3D0CeCB2zc7qHRycca7c9bb"
ENTERED_USERS_DB = os.getenv('ENTERED_USERS_DB')

class CheckingForQueue(SystemState):
    def init(self):
        ev = self.context.sessions_queue.get() # guarantee CARD_IN_VALID or CARD_OUT_VALID or INTERCOM_OVERRIDE. tmp: CARD_OUT_TAP
        if ev.type is EventType.INTERCOM_OVERRIDE: # pass special access
            pass
        # elif ev.type is EventType.CARD_OUT_TAP:
        #     pass
        else:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }

            uid = ev.payload["uid"]

            try:
                if ev.type is EventType.CARD_IN_VALID:
                    # INSERT
                    response = requests.post(
                        API_BASE_URL,
                        json={
                            "uid": uid
                        },
                        headers=headers
                    )

                else:
                    # DELETE
                    response = requests.delete(
                        f"{API_BASE_URL}/{uid}",
                        headers=headers
                    )

                    response.raise_for_status()

            except requests.RequestException as e:
                print(f"API request failed: {e}")

            if self.context.sessions_queue.empty():
                self.context.set_state("ClosingGate")
                return

            self.context.set_state("WaitingForVehicleGone")
        
    def execute(self):
        pass
