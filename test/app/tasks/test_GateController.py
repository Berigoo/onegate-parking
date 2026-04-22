import pytest
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import GateController
from app.core import SessionQueue
from app.domain import StateEvent, EventType
import time
from bsp import bsp

class TestGateControllerHWTests:
    def test_when_open(self):        # pls pay attentiona to relay 'click' sound
        bsp.bsp_init()
        gate = GateController()
        gate.open()
        time.sleep(1)

    def test_when_close(self):
        bsp.bsp_init()
        gate = GateController()
        gate.close()
        time.sleep(1)

    def test_when_close(self):
        bsp.bsp_init()
        gate = GateController()
        gate.open()
        gate.hold()
        time.sleep(1)
