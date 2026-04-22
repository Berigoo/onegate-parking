import pytest
import time
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import IntercomRelayMonitor
from app.core import SessionQueue
from app.domain import StateEvent, EventType
from bsp import bsp

class TestIntercomRelayMonitorThreading:
    def test_start_creates_thread(self):
        bsp.bsp_init()
        queue = SessionQueue()
        intercom_relay_monitor = IntercomRelayMonitor(queue)

        assert intercom_relay_monitor.thread is None
        assert not intercom_relay_monitor.running

        intercom_relay_monitor.start()

        assert intercom_relay_monitor.thread is not None
        assert intercom_relay_monitor.running
        assert intercom_relay_monitor.thread.daemon is True

    def test_start_prevents_duplicate_threads(self):
        bsp.bsp_init()
        queue = SessionQueue()
        intercom_relay_monitor = IntercomRelayMonitor(queue)

        intercom_relay_monitor.start()
        first_thread = intercom_relay_monitor.thread

        intercom_relay_monitor.start()
        second_thread = intercom_relay_monitor.thread

        assert first_thread is second_thread

    def test_stop_gracefully_stops_thread(self):
        bsp.bsp_init()
        queue = SessionQueue()
        intercom_relay_monitor = IntercomRelayMonitor(queue)

        # Mock the _run method to avoid actual execution
        intercom_relay_monitor._run = Mock()
        intercom_relay_monitor.start()

        assert intercom_relay_monitor.running

        intercom_relay_monitor.stop()

        assert not intercom_relay_monitor.running
        # Thread should complete within timeout
        intercom_relay_monitor.thread.join(timeout=2)
        assert not intercom_relay_monitor.thread.is_alive()

class TestIntercomBasicFunctionalitites:
    def test_when_intercom_relay_high(self):
        bsp.bsp_init()
        queue = SessionQueue()
        intercom = IntercomRelayMonitor(queue)

        intercom._IntercomRelayMonitor__when_intercom_relay_high()

        ev = queue.get()
        assert ev.type is EventType.INTERCOM_OVERRIDE

class TestIntercomHWTests:
    def test_when_pin_pulled_high(self):
        bsp.bsp_init()
        queue = SessionQueue()
        intercom = IntercomRelayMonitor(queue)
        intercom.start()

        time.sleep(2)

        count = queue.qsize()
        assert count > 0
        
