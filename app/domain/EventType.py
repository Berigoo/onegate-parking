from enum import Enum

class EventType(Enum):
    CARD_IN_VALID = "card_in_valid"
    CARD_OUT_VALID = "card_out_valid"
    VEHICLE_DETECTED = "vehicle_detected"
    VEHICLE_GONE = "vehicle_gone"
    INTERCOM_OVERRIDE = "intercom_override"


