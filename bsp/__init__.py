from config import OPI_ZERO

if OPI_ZERO:
    from bsp.opizero import BSP
else:
    class BSP:
        def __init__(self):
            pass

        def read_vld_in(self):
            return False

        def read_vld_out(self):
            return False

        def read_intercom_relay(self):
            return False

        def write_boom_gate(self, state):
            pass

        def on_vld_in_high(self, cb):
            pass

        def on_vld_out_high(self, cb):
            pass

__all__ = ['BSP']
