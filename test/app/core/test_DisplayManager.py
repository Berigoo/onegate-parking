import pytest
import numpy as np
import cv2
import time
from unittest.mock import Mock, MagicMock, patch, call
from app.core import DisplayManager
from app.tasks import CameraMonitor, DisplayWorker
from dotenv import load_dotenv


class TestDisplayManagerBasicFunctionalities:
    def test_render_with_frame(self):
        load_dotenv()

        dw = DisplayWorker()
        dw.start()
        c = CameraMonitor()
        c.stream_handle(dw.show)
        c.start()

        while True:
            True
