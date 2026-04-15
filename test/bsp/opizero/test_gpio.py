import pytest
from unittest.mock import MagicMock, patch
from bsp import bsp

def test_init_calls_gpio_init():
    with patch('bsp.opizero.gpio') as mock_gpio:
        bsp.bsp_init()
        mock_gpio.init_gpio.assert_called_once()

def test_read_vld_in_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        mock_gpio.read_vld_in.return_value = True
        
        assert bsp.bsp_read_vld_in() == True
        mock_gpio.read_vld_in.assert_called_once()

def test_read_intercom_relay_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        mock_gpio.read_intercom_relay1.return_value = True

        assert bsp.bsp_read_intercom_relay() == True
        mock_gpio.read_intercom_relay1.assert_called_once()        

def test_write_boom_gate_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        bsp.bsp_write_boom_gate(True)
        mock_gpio.write_boom_gate.assert_called_once_with(True)

def test_on_vld_in_high_registers_callback():
    with patch('bsp.opizero.gpio') as mock_gpio:
        callback = MagicMock()
        bsp.bsp_on_vld_in_high(callback)
        mock_gpio.on_vld_in_high.assert_called_once_with(callback)
