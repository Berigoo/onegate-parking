from .Idle import Idle
from .HoldingGate import HoldingGate
from .OpeningGate import OpeningGate
from .ClosingGate import ClosingGate
from .SerialDataProcessing import SerialDataProcessing
from .WaitingForEmoneyTap import WaitingForEmoneyTap
from .WaitingForVehicleGone import WaitingForVehicleGone

STATE_MAP = {
    "Idle": Idle,
    "OpeningGate": OpeningGate,
    "HoldingGate": HoldingGate,
    "ClosingGate": ClosingGate,
    "SerialDataProcessing": SerialDataProcessing,
    "WaitingForEmoneyTap": WaitingForEmoneyTap,
    "WaitingForVehicleGone": WaitingForVehicleGone
}

__all__ = ['STATE_MAP']
