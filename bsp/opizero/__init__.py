from . import gpio

class BSP:
    def __init__(self):
        gpio.init_gpio()
        
    def read_vld_in(self):
        return gpio.read_vld_in()
    
    def read_vld_out(self):
        return gpio.read_vld_out()

    def read_intercom_relay(self):
        return gpio.read_intercom_relay1()

    def write_boom_gate(self, state):
        gpio.write_boom_gate(state)

    def on_vld_in_high(self, cb):
        gpio.on_vld_in_high(cb)

    def on_vld_out_high(self, cb):
        gpio.on_vld_out_high(cb)        

    def stream_rtsp(self, source):
        # TODO 
        pass
            
