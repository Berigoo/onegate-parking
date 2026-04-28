import serial
import threading
import mariadb
import time
import os
from app.domain import StateEvent, EventType
from app.core import SessionQueue, Logger

# Expected length of a card data payload (heuristic used by parser)
CARD_DATA_LEN = 21
FRAME_LEN = CARD_DATA_LEN + 4
USERS_DB=os.getenv('USERS_DB')
DB_CONF = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "laravel",
    "password": "",
    "database": "onegate_parkinng_dashboard"
}

class CardValidatorIn:
    def __init__(self, port, queue_to_push: SessionQueue, db=DB_CONF):
        self.port = port
        self.db = db
        self.queue = queue_to_push
        self.serial = None
        self.running = False
        self.thread = None
        self.logger = Logger("CardValidatorIn")

    #################### threading methods
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    def _run(self):
        self.__setup()
        while self.running:
            self.__loop()
            time.sleep(0.01)
    ####################

    #################### Task Logic
    def __setup(self):
        # Attempt to connect to the serial device; keep self.serial in a valid state
        self.serial = self.__serial_connect(self.port)
    def __loop(self):
        if self.serial is None:
            self.__serial_reconnect()
        else:
            if self.serial.in_waiting > 0:
                event = StateEvent(
                    type=EventType.CARD_TAP,
                    payload=None
                )
                self.queue.put(event)
                raw_data = self.__read_exact(FRAME_LEN)
                try:
                    if raw_data:
                        data = self.__parse(raw_data)
                        is_valid = self.__validate(data)
                        obj = {
                            "uid": data["uid"],
                            "number": data["number"],
                            "is_valid": is_valid
                        }
                        event = StateEvent(
                            type=EventType.CARD_IN_VALID,
                            payload=obj
                        )
                        self.queue.put(event)
                except Exception as e:
                    self.logger.warning("Kartu tidak valid atau sistem gagal")

    
    def __read_exact(self, size):
        buffer = b""
        while len(buffer) < size:
            chunk = self.serial.read(size - len(buffer))
            if not chunk:
                return None  # timeout or disconnected
            buffer += chunk
            print(buffer)
        return buffer
    
    def __parse(self, raw_data):
        if raw_data is None or len(raw_data) < CARD_DATA_LEN:
            return None
        try:
            payload = raw_data[3:-1]
            if len(payload) < 21:
                self.logger.debug("Payload too short after trimming")
                return None

            # byte slicing (clean & aligned with protocol)
            offset = 0

            card_type = payload[offset:offset+1]
            offset += 1

            card_uid = payload[offset:offset+7]
            offset += 7

            validity = payload[offset:offset+1]
            offset += 1

            card_number = payload[offset:offset+8]
            offset += 8

            balance = payload[offset:offset+4]

            return {
                "types": card_type.hex(),
                "uid": card_uid.hex(),
                "validity": validity.hex(),
                "number": card_number.hex(),
                "balance": balance.hex(),
                "card_info": payload.hex()
            }
        
        except Exception as e:
            self.logger.debug(f"Parse error: {e}")
            return None

    def __validate(self, data):
        try:
            conn = mariadb.connect(**self.db)
            cursor = conn.cursor(dictionary=True)

            # Check if uid or number exists
            cursor.execute(
                "SELECT 1 FROM user_cards WHERE uid = ?",
                (data["number"],)
            )
            result = cursor.fetchone()
            is_valid = result is not None
            conn.close()

            if is_valid:
                data["name"] = result["nama"] # name supplied when valid
                self.logger.info(f"Card valid: uid={data['uid']}")
            else:
                self.logger.warning(f"Card not found: uid={data['uid']}")

            return is_valid
        except Exception as e:
            self.logger.error(f"Database error during validation: {e}")
            return False
        
    def __serial_connect(self, port):
        retries = 5
        while retries > 0:
            try:
                ser = serial.Serial(
                    port=port,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1,
                )
                return ser
            except serial.SerialException as e:
                self.logger.warning(f"Failed to connect to serial. retrying...: {e}")
                retries -= 1
                time.sleep(0.2)
        return None

    def __serial_reconnect(self):
        self.serial = self.__serial_connect(self.port)
        ####################
