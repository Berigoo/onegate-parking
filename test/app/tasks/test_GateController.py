import pytest
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import GateController
from app.core import SessionQueue
from app.domain import StateEvent, EventType
import time
from bsp import bsp

class TestGateControllerHWTests:
    def test_when_open_close_hold(self):        # pls pay attentiona to relay 'click' sound
        bsp.bsp_init()
        gate = GateController()
        gate.open()
        time.sleep(3)
        gate.close()
        time.sleep(3)
        gate.hold()
