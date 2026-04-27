import os
import serial
import threading
import mariadb
from app.domain import StateEvent, EventType
from app.core import SessionQueue, Logger

CARD_DATA_LEN=21
USERS_DB=os.getenv('USERS_DB')
DB_CONF = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "laravel",
    "password": "",
    "database": "onegate_parkinng_dashboard"
}

class CardValidatorOut:
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
        self.serial = self.__serial_connect(self.port)
    def __loop(self):
        if self.serial is None:
            self.serial_reconnect()
        if self.serial.in_waiting > 0:
            event = StateEvent(
                        type=EventType.CARD_TAP,
                        payload=None
                    )
            self.queue.put(event)
            raw_data = self.serial.readline()
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
                        type=EventType.CARD_OUT_VALID,
                        payload=obj
                    )
                    self.queue.put(event)
            except Exception as e:
                self.logger.warning("Kartu tidak valid atau sistem gagal", e)

    def __parse(self, raw_data):
        if raw_data is None or len(raw_data) < CARD_DATA_LEN:
            return None
        try:
            data = raw_data[3:-1].hex() # assume first 3 bytes is a metadata, and last byte is a terminator
            card_types = data[:2]
            card_uid = data[2:2+14]
            card_val = data[16:16+2]
            card_num = data[18:18+16]
            balance = data[34:34+8]
            return {
                "types":(card_types),
                "uid":(card_uid),
                "validity":(card_val),
                "number":(card_num),
                "balance":(balance),
                "card_info":data
            }
        except Exception as e:
            self.logger.debug(f"Parse error: {e}")
        return None

    def __validate(self, data):
        try:
            conn = mariadb.connect(**self.db)
            cursor = conn.cursor()

            # Check if uid or number exists
            cursor.execute(
                "SELECT 1 FROM user_cards WHERE uid = ?",
                (data["uid"],)
            )
            result = cursor.fetchone() is not None
            conn.close()

            if result:
                self.logger.info(f"Card valid: uid={data['uid']}")
            else:
                self.logger.warning(f"Card not found: uid={data['uid']}")

            return result
        except Exception as e:
            self.logger.error("Database error during validation", e)
            return False
        
    def __serial_connect(self, port):
        while self.serial is None:
            try:
                self.serial = serial.Serial(
                    port=port,
                    baudrate=9600,        
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS)
            except serial.SerialException as e:
                self.logger.warning("Failed to connect to serial. retyring...", e)
    def __serial_reconnect(self):
        self.__serial_connect(self.port)
        ####################
