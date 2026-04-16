from .interface import BSP

# Prefer OPi Zero implementation for testability in CI environments.
# If that import fails (e.g. on a real Raspberry Pi), fall back to Raspi.
try:
    from bsp.opizero import BSPOpiZero as _impl
except Exception:
    try:
        from bsp.raspi import BSPRaspi as _impl
    except Exception:
        _impl = None

bsp = BSP(_impl()) if _impl is not None else BSP(None)
