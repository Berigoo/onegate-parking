from . import config
import gpiozero
import time

# Fallback dummy pin devices for environments without GPIO hardware or
# gpiozero pin factories installed. This helps running unit tests in CI.
class _DummyInputDevice:
    def __init__(self, *args, **kwargs):
        self.value = False
        self.when_activated = None
        self.when_deactivated = None

class _DummyOutputDevice:
    def __init__(self, *args, **kwargs):
        pass
    def on(self):
        pass
    def off(self):
        pass

_VLD_IN = None
_INTERCOM_RELAY1 = None
_BOOM_GATE_HIGH = None
_BOOM_GATE_LOW = None

def init_gpio():
    global _VLD_IN, _INTERCOM_RELAY1, _BOOM_GATE_HIGH, _BOOM_GATE_LOW
    try:
        # input devices
        _VLD_IN = gpiozero.DigitalInputDevice(config.PIN_IN_VLD, pull_up=False, bounce_time=2)
        _INTERCOM_RELAY1 = gpiozero.DigitalInputDevice(config.PIN_IN_INTERCOM_RELAY1, pull_up=False, bounce_time=2)

        # output device
        _BOOM_GATE_HIGH = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_HIGH, active_high=True, initial_value=True)
        _BOOM_GATE_LOW = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_LOW, active_high=True, initial_value=True)
    except Exception:
        # Fallback to dummy devices when hardware libraries are unavailable
        _VLD_IN = _DummyInputDevice()
        _INTERCOM_RELAY1 = _DummyInputDevice()
        _BOOM_GATE_HIGH = _DummyOutputDevice()
        _BOOM_GATE_LOW = _DummyOutputDevice()

def read_vld_in():      # read in vld state
    return _VLD_IN.value
    
def read_intercom_relay1(): # read intercom relay1 state
    return _INTERCOM_RELAY1.value

def write_boom_gate(state):
    if state is True:
        _BOOM_GATE_HIGH.on()
        _BOOM_GATE_LOW.off()
    else:
        _BOOM_GATE_HIGH.off()
        _BOOM_GATE_LOW.on()
        
def write_boom_gate_hold():
    _BOOM_GATE_HIGH.on()
    _BOOM_GATE_LOW.on()

def on_vld_in_high(cb): # execute 'cb' when in vld is HIGH 
    _VLD_IN.when_activated = cb
    
def on_vld_in_low(cb):
    _VLD_IN.when_deactivated = cb

def on_intercom_relay_high(cb):
    _INTERCOM_RELAY1.when_activated = cb
