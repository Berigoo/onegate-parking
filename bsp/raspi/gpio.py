from . import config
import RPi.GPIO as GPIO
import time

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    
    # input devices
    GPIO.setup(config.PIN_IN_VLD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(config.PIN_IN_INTERCOM_RELAY1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    # output device
    GPIO.setup(config.PIN_BOOM_GATE_HIGH, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(config.PIN_BOOM_GATE_LOW, GPIO.OUT, initial=GPIO.HIGH)

def read_vld_in():      # read in vld state
    return GPIO.input(config.PIN_IN_VLD)
    
def read_intercom(): # read intercom relay1 state
    return GPIO.input(config.PIN_IN_INTERCOM_RELAY1)

def write_boom_gate(state):
    if state is True:
        GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.HIGH)
        GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.LOW)
    else:
        GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.LOW)
        GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.HIGH)
        
def write_boom_gate_hold():
    GPIO.output(config.PIN_BOOM_GATE_HIGH, GPIO.LOW)
    GPIO.output(config.PIN_BOOM_GATE_LOW, GPIO.LOW)

def on_vld_in_high(cb): # execute 'cb' when in vld is HIGH
    GPIO.add_event_detect(config.PIN_IN_VLD, GPIO.RISING, callback=cb, bouncetime=2000)
    
def on_vld_in_low(cb):
    GPIO.add_event_detect(config.PIN_IN_VLD, GPIO.FALLING, callback=cb, bouncetime=2000)

def on_intercom_relay_high(cb):
    GPIO.add_event_detect(config.PIN_IN_INTERCOM_RELAY1, GPIO.RISING, callback=cb, bouncetime=2000)
