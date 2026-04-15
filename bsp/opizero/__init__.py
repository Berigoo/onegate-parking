from . import gpio

def bsp_init():
    gpio.init_gpio()
        
def bsp_read_vld_in():
    return gpio.read_vld_in()
    
def bsp_read_vld_out():
    return gpio.read_vld_out()

def bsp_on_vld_in_high(cb):
    gpio.on_vld_in_high(cb)

def bsp_on_vld_out_high(cb):
    gpio.on_vld_out_high(cb)        

def bsp_read_intercom_relay():
    return gpio.read_intercom_relay1()

def bsp_write_boom_gate(state):
    gpio.write_boom_gate(state)

def bsp_write_boom_gate_hold():
    gpio.write_boom_gate_hold()


