from abc import ABC, abstractmethod
from typing import Callable

class BSPInterface(ABC):
    @abstractmethod
    def bsp_init(self) -> None: ...

    @abstractmethod
    def bsp_read_vld_in(self) -> bool: ...

    @abstractmethod
    def bsp_on_vld_in_high(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def bsp_on_vld_in_low(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def bsp_read_intercom_relay(self) -> bool: ...

    @abstractmethod
    def bsp_on_intercom_relay_high(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def bsp_write_boom_gate(self, state: bool) -> None: ...

    @abstractmethod
    def bsp_write_boom_gate_hold(self) -> None: ...


class BSP:
    def __init__(self, impl: BSPInterface):
        self._impl = impl
    def bsp_init(self):
        self._impl.bsp_init()
    def bsp_read_vld_in(self):
        return self._impl.bsp_read_vld_in()
    def bsp_on_vld_in_high(self, callback):
        self._impl.bsp_on_vld_in_high(callback)
    def bsp_on_vld_in_low(self, callback):
        # Pass the callback directly to the underlying implementation
        self._impl.bsp_on_vld_in_low(callback)
    def bsp_read_intercom_relay(self):
        return self._impl.bsp_read_intercom_relay()
    def bsp_on_intercom_relay_high(self, callback):
        self._impl.bsp_on_intercom_relay_high(callback)
    def bsp_write_boom_gate(self, state):
        self._impl.bsp_write_boom_gate(state)
    def bsp_write_boom_gate_hold(self):
        self._impl.bsp_write_boom_gate_hold()
