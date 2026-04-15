from config import OPI_ZERO
from .interface import BSP

if OPI_ZERO:
    from bsp.opizero import BSPOpiZero as _impl
else:
    pass                        # TODO

bsp = BSP(_impl())
