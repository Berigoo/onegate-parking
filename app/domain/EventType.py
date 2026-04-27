from enum import Enum

class EventType(Enum):
    GENERIC_TIMEOUT = "generic_timeout"
    CARD_TAP = "card_tap"
    CARD_IN_VALID = "card_in_valid"
    CARD_OUT_VALID = "card_out_valid"
    VEHICLE_DETECTED = "vehicle_detected"
    VEHICLE_GONE = "vehicle_gone"
    INTERCOM_OVERRIDE = "intercom_override"
    ASKING_FOR_SHUTDOWN = "asking_for_shutdown"
    CARD_REGISTER = "card_register"


