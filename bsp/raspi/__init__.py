from ..interface import BSPInterface
from . import gpio

class BSPRaspi(BSPInterface):
    def bsp_init(self):
        gpio.init_gpio()
        
    def bsp_read_vld_in(self):
        return gpio.read_vld_in()

    def bsp_read_intercom(self):
        return gpio.read_intercom()

    def bsp_on_vld_in_high(self, cb):
        gpio.on_vld_in_high(cb)

    def bsp_on_vld_in_low(self, cb):
        gpio.on_vld_in_low(cb)

    def bsp_read_intercom_relay(self):
        return gpio.read_intercom_relay1()

    def bsp_on_intercom_relay_high(self, cb):
        gpio.on_intercom_relay_high(cb)

    def bsp_write_boom_gate(self, state):
        gpio.write_boom_gate(state)

    def bsp_write_boom_gate_hold(self):
        gpio.write_boom_gate_hold()


