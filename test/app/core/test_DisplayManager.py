import pytest
import numpy as np
from unittest.mock import Mock, MagicMock, patch, call
from app.core import DisplayManager

class TestDisplayManagerBasicFunctionalities:
    def test_a_singleton(self):
        dm = DisplayManager()
        dm2 = DisplayManager()

        assert dm == dm2

    def test_render_with_frame_none(self):
        dm = DisplayManager()
        dm.render(None)

    def test_render_with_frame(self):
        dm = DisplayManager()
        frame = np.full((480, 854, 3), (255, 200, 100), dtype=np.uint8) # light blue dummy frame

        dm.render(frame)
        
    
