from . import config
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
Device.pin_factory = LGPIOFactory()

import gpiozero
# import RPi.GPIO as GPIO
import time

_VLD = None
_INTERCOM = None
_GATE_HIGH = None
_GATE_LOW = None

def init_gpio():
    global _VLD, _INTERCOM, _GATE_HIGH, _GATE_LOW
    # GPIO.setmode(GPIO.BCM)
    
    # # input devices
    # GPIO.setup(config.PIN_IN_VLD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(config.PIN_IN_INTERCOM_RELAY1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    # # output device
    # GPIO.setup(config.PIN_BOOM_GATE_HIGH, GPIO.OUT, initial=GPIO.HIGH)
    # GPIO.setup(config.PIN_BOOM_GATE_LOW, GPIO.OUT, initial=GPIO.HIGH)

    _VLD = gpiozero.DigitalInputDevice(config.PIN_IN_VLD, pull_up=True, bounce_time=2)
    _INTERCOM = gpiozero.DigitalInputDevice(config.PIN_IN_INTERCOM_RELAY1, pull_up=True, bounce_time=2)

    _GATE_HIGH = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_HIGH, active_high=True, initial_value=False)
    _GATE_LOW = gpiozero.DigitalOutputDevice(config.PIN_BOOM_GATE_LOW, active_high=True, initial_value=True)

def deinit_gpio():
    # GPIO.cleanup()
    pass
    
def read_vld_in():      # read in vld state
    global _VLD
    return _VLD.value
    # return GPIO.input(config.PIN_IN_VLD)
    
def read_intercom(): # read intercom relay1 state
    global _INTERCOM
    return _INTERCOM.value
    # return GPIO.input(config.PIN_IN_INTERCOM_RELAY1)

def write_boom_gate(state):
    global _GATE_HIGH, _GATE_LOW
    if state is True:
        _GATE_HIGH.on()
        _GATE_LOW.off()
        # GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.HIGH)
        # GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.LOW)
    else:
        _GATE_HIGH.off()
        _GATE_LOW.on()
        # GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.LOW)
        # GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.HIGH)
        
def write_boom_gate_hold():
    global _GATE_HIGH, _GATE_LOW
    _GATE_HIGH.off()
    _GATE_LOW.on()
    # GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.HIGH)
    # GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.LOW)

def on_vld_in_high(cb): # execute 'cb' when in vld is HIGH
    global _VLD
    _VLD.when_activated = cb
    # GPIO.add_event_detect(config.PIN_IN_VLD, GPIO.RISING, callback=cb, bouncetime=2000)
    
def on_vld_in_low(cb):
    global _VLD
    _VLD.when_deactivated = cb
    # GPIO.add_event_detect(config.PIN_IN_VLD, GPIO.FALLING, callback=cb, bouncetime=2000)

def on_intercom_relay_high(cb):
    global _INTERCOM
    _INTERCOM.when_activated = cb
    # GPIO.add_event_detect(config.PIN_IN_INTERCOM_RELAY1, GPIO.RISING, callback=cb, bouncetime=2000)
