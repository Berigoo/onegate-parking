from .interface import BSP

if OPI_ZERO:
    from bsp.opizero import BSPOpiZero as _impl
else:
    from bsp.raspi import BSPRaspi as _impl

bsp = BSP(_impl()) if _impl is not None else BSP(None)
