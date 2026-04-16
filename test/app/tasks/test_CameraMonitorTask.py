import pytest
from unittest.mock import Mock, MagicMock, patch, call
from app.tasks import CameraMonitor
from app.core import SessionQueue
from app.domain import StateEvent, EventType

@patch('app.tasks.CameraMonitorTask.cv2.VideoCapture')
class TestCameraMonitorThreading:
    def test_start_creates_thread(self, mock):
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = True
        mock_cam.read.return_value = (None, None)
        mock.return_value = mock_cam

        camera_monitor = CameraMonitor()

        assert camera_monitor.thread is None
        assert not camera_monitor.running

        camera_monitor.start()

        assert camera_monitor.thread is not None
        assert camera_monitor.running
        assert camera_monitor.thread.daemon is True

    def test_start_prevents_duplicate_threads(self, mock):
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = True
        mock_cam.read.return_value = (None, None)
        mock.return_value = mock_cam
        
        camera_monitor = CameraMonitor()

        camera_monitor.start()
        first_thread = camera_monitor.thread

        camera_monitor.start()
        second_thread = camera_monitor.thread

        assert first_thread is second_thread

    def test_stop_gracefully_stops_thread(self, mock):
        camera_monitor = CameraMonitor()

        # Mock the _run method to avoid actual execution
        camera_monitor._run = Mock()
        camera_monitor.start()

        assert camera_monitor.running

        camera_monitor.stop()

        assert not camera_monitor.running
        # Thread should complete within timeout
        camera_monitor.thread.join(timeout=2)
        assert not camera_monitor.thread.is_alive()

# TODO testing its funcs

    
