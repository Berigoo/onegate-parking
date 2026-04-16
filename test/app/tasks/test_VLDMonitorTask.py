import pytest
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import VLDMonitor
from app.core import SessionQueue
from app.domain import StateEvent, EventType

class TestVLDMonitorThreading:
    def test_start_creates_thread(self):
        queue = SessionQueue()
        vldmonitor = VLDMonitor(queue)

        assert vldmonitor.thread is None
        assert not vldmonitor.running

        vldmonitor.start()

        assert vldmonitor.thread is not None
        assert vldmonitor.running
        assert vldmonitor.thread.daemon is True

    def test_start_prevents_duplicate_threads(self):
        queue = SessionQueue()
        vldmonitor = VLDMonitor(queue)

        vldmonitor.start()
        first_thread = vldmonitor.thread

        vldmonitor.start()
        second_thread = vldmonitor.thread

        assert first_thread is second_thread

    def test_stop_gracefully_stops_thread(self):
        queue = SessionQueue()
        vldmonitor = VLDMonitor(queue)

        # Mock the _run method to avoid actual execution
        vldmonitor._run = Mock()
        vldmonitor.start()

        assert vldmonitor.running

        vldmonitor.stop()

        assert not vldmonitor.running
        # Thread should complete within timeout
        vldmonitor.thread.join(timeout=2)
        assert not vldmonitor.thread.is_alive()


class TestVLDMonitorBasicFunctionalitites:
    @patch('app.tasks.VLDMonitorTask.bsp')
    def test_get_state_delegated(self, mock):
            queue = SessionQueue()
            vldmonitor = VLDMonitor(queue)
            mock.bsp_read_vld_in.return_value = True

            assert vldmonitor.get_state() is True
            mock.bsp_read_vld_in.assert_called_once()

    def test_when_vld_high(self):
        queue = SessionQueue()
        vldmonitor = VLDMonitor(queue)

        vldmonitor._VLDMonitor__when_vld_high()

        ev = queue.get()
        assert ev.type is EventType.VEHICLE_DETECTED

    def test_when_vld_low(self):
        queue = SessionQueue()
        vldmonitor = VLDMonitor(queue)

        vldmonitor._VLDMonitor__when_vld_low()

        ev = queue.get()
        assert ev.type is EventType.VEHICLE_GONE
            
        


            
        

