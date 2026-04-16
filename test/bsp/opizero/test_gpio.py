import pytest
from unittest.mock import MagicMock, patch
from bsp import bsp

@patch('bsp.opizero.gpio')
def test_init_calls_gpio_init(mock):
    bsp.bsp_init()
    mock.init_gpio.assert_called_once()

@patch('bsp.opizero.gpio')
def test_read_vld_in_delegates_to_gpio(mock):
    mock.read_vld_in.return_value = True
        
    assert bsp.bsp_read_vld_in() is True
    mock.read_vld_in.assert_called_once()

@patch('bsp.opizero.gpio')        
def test_read_intercom_relay_delegates_to_gpio(mock):
    mock.read_intercom_relay1.return_value = True

    assert bsp.bsp_read_intercom_relay() == True
    mock.read_intercom_relay1.assert_called_once()        

@patch('bsp.opizero.gpio')        
def test_write_boom_gate_delegates_to_gpio(mock):
    bsp.bsp_write_boom_gate(True)
    mock.write_boom_gate.assert_called_once_with(True)

@patch('bsp.opizero.gpio')        
def test_on_vld_in_high_registers_callback(mock):
    callback = MagicMock()
    bsp.bsp_on_vld_in_high(callback)
    mock.on_vld_in_high.assert_called_once_with(callback)
