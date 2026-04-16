from config import OPI_ZERO, RASPI
from .interface import BSP

if OPI_ZERO:
    from bsp.opizero import BSPOpiZero as _impl
elif RASPI:
    from bsp.raspi import BSPRaspi as _impl
else:
    pass                        # TODO

bsp = BSP(_impl())
