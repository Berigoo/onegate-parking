import os
from .interface import BSP

OPI_ZERO = os.getenv('OPI_ZERO', 'false').lower() in ('true', '1', 'yes')
RASPI = os.getenv('RASPI', 'false').lower() in ('true', '1', 'yes')

if OPI_ZERO:
    from bsp.opizero import BSPOpiZero as _impl
else:
    from bsp.raspi import BSPRaspi as _impl

bsp = BSP(_impl()) if _impl is not None else BSP(None)
