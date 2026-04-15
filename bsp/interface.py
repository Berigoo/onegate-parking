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
        self.bsp_init = impl.bsp_init
        self.bsp_read_vld_in = impl.bsp_read_vld_in
        self.bsp_on_vld_in_high = impl.bsp_on_vld_in_high
        self.bsp_on_vld_in_low = impl.bsp_on_vld_in_low
        self.bsp_read_intercom_relay = impl.bsp_read_intercom_relay
        self.bsp_on_intercom_relay_high = impl.bsp_on_intercom_relay_high
        self.bsp_write_boom_gate = impl.bsp_write_boom_gate
        self.bsp_write_boom_gate_hold = impl.bsp_write_boom_gate_hold
