from . import config
import gpiozero 

_VLD_IN  = None
_VLD_OUT = None
_INTERCOM_RELAY1 = None
_BOOM_GATE_HIGH = None
_BOOM_GATE_LOW = None

def init_gpio():
    global _VLD_IN, _VLD_OUT, _INTERCOM_RELAY1, _BOOM_GATE
    
    # input devices
    _VLD_IN = gpiozero.DigitalInputDevice(config.PIN_IN_VLD, False, bounce_time=2) # in VLD sensor, pulled-down, ignore change for next 2s 
    _VLD_OUT = gpiozero.DigitalInputDevice(config.PIN_OUT_VLD, False, bounce_time=2) # out VLD sensor, pulled-down, ignore change for next 2s
    _INTERCOM_RELAY1 = gpiozero.DigitalInputDevice(config.PIN_IN_INTERCOM_RELAY1, False, bounce_time=2) # in intercom relay signal, pulled-down, ignore change for next 2s

        # output device
    _BOOM_GATE_HIGH = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_HIGH, True, False); # boom gate pin, active-high, LOW initial state
    _BOOM_GATE_LOW = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_LOW, True, False);

def read_vld_in():      # read in vld state
    return _VLD_IN.value
    
def read_vld_out():     # read out vld state
    return _VLD_OUT.value

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

def on_vld_out_high(cb): # execute 'cb' when out vld is HIGH 
    _VLD_OUT.when_activated = cb
            
