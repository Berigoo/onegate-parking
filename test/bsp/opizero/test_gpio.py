import pytest
from unittest.mock import MagicMock, patch
from bsp.opizero import BSP

def test_init_calls_gpio_init():
    with patch('bsp.opizero.gpio') as mock_gpio:
        bsp = BSP()
        mock_gpio.init_gpio.assert_called_once()

def test_read_vld_in_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        mock_gpio.read_vld_in.return_value = True
        bsp = BSP()
        assert bsp.read_vld_in() == True
        mock_gpio.read_vld_in.assert_called_once()

def test_read_vld_out_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        mock_gpio.read_vld_out.return_value = True
        bsp = BSP()
        assert bsp.read_vld_out() == True
        mock_gpio.read_vld_out.assert_called_once()

def test_read_intercom_relay_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        mock_gpio.read_intercom_relay1.return_value = True
        bsp = BSP()
        assert bsp.read_intercom_relay() == True
        mock_gpio.read_intercom_relay1.assert_called_once()        

def test_write_boom_gate_delegates_to_gpio():
    with patch('bsp.opizero.gpio') as mock_gpio:
        bsp = BSP()
        bsp.write_boom_gate(True)
        mock_gpio.write_boom_gate.assert_called_once_with(True)

def test_on_vld_in_high_registers_callback():
    with patch('bsp.opizero.gpio') as mock_gpio:
        bsp = BSP()
        callback = MagicMock()
        bsp.on_vld_in_high(callback)
        mock_gpio.on_vld_in_high.assert_called_once_with(callback)
