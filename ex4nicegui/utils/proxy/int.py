from __future__ import annotations
from typing import (
    Literal,
    Optional,
    SupportsIndex,
    Tuple,
    Union,
)
import sys
from . import utils
from .base import Proxy


class IntProxy(Proxy):
    # def __new__(cls, value):
    #     return super().__new__(cls, value)

    def __init__(self, value: int):
        from ex4nicegui.utils.signals import to_ref

        self._ref = to_ref(value)

    def __str__(self) -> str:
        return str(self._ref.value)

    def as_integer_ratio(self) -> Tuple[int, Literal[1]]:
        return self._ref.value.as_integer_ratio()

    @property
    def real(self) -> int:
        return self._ref.value.real

    @property
    def imag(self) -> Literal[0]:
        return 0

    @property
    def numerator(self) -> int:
        return self._ref.value.numerator

    @property
    def denominator(self) -> Literal[1]:
        return 1

    def conjugate(self) -> int:
        return self._ref.value.conjugate()

    def bit_length(self) -> int:
        return self._ref.value.bit_length()

    if sys.version_info >= (3, 10):

        def bit_count(self) -> int:
            return self._ref.value.bit_count()

    if sys.version_info >= (3, 11):

        def to_bytes(
            self,
            length: SupportsIndex = 1,
            byteorder: Literal["little", "big"] = "big",
            *,
            signed: bool = False,
        ) -> bytes:
            return self._ref.value.to_bytes(length, byteorder, signed=signed)

    else:

        def to_bytes(
            self,
            length: SupportsIndex,
            byteorder: Literal["little", "big"],
            *,
            signed: bool = False,
        ) -> bytes:
            return self._ref.value.to_bytes(length, byteorder, signed=signed)

    if sys.version_info >= (3, 12):

        def is_integer(self) -> Literal[True]:
            return True

    def __add__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__add__(int(utils.to_value(value)))

    def __sub__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__sub__(int(utils.to_value(value)))

    def __mul__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__mul__(int(utils.to_value(value)))

    def __floordiv__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__floordiv__(int(utils.to_value(value)))

    def __truediv__(self, value: Union[int, IntProxy]) -> float:
        return self._ref.value.__truediv__(int(utils.to_value(value)))

    def __mod__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__mod__(int(utils.to_value(value)))

    def __divmod__(self, value: Union[int, IntProxy]) -> Tuple[int, int]:
        return self._ref.value.__divmod__(int(utils.to_value(value)))

    def __radd__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__radd__(int(utils.to_value(value)))

    def __rsub__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rsub__(int(utils.to_value(value)))

    def __rmul__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rmul__(int(utils.to_value(value)))

    def __rfloordiv__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rfloordiv__(int(utils.to_value(value)))

    def __rtruediv__(self, value: Union[int, IntProxy]) -> float:
        return self._ref.value.__rtruediv__(int(utils.to_value(value)))

    def __rmod__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rmod__(int(utils.to_value(value)))

    def __rdivmod__(self, value: Union[int, IntProxy]) -> Tuple[int, int]:
        return self._ref.value.__rdivmod__(int(utils.to_value(value)))

    def __pow__(
        self, value: Union[int, IntProxy], mod: Optional[int] = None
    ) -> Union[int, float]:
        return self._ref.value.__pow__(int(utils.to_value(value)), mod)

    def __rpow__(
        self, value: Union[int, IntProxy], mod: Optional[int] = None
    ) -> Union[int, float]:
        return self._ref.value.__rpow__(int(utils.to_value(value)), mod)

    def __and__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__and__(int(utils.to_value(value)))

    def __or__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__or__(int(utils.to_value(value)))

    def __xor__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__xor__(int(utils.to_value(value)))

    def __lshift__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__lshift__(int(utils.to_value(value)))

    def __rshift__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rshift__(int(utils.to_value(value)))

    def __rand__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rand__(int(utils.to_value(value)))

    def __ror__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__ror__(int(utils.to_value(value)))

    def __rxor__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rxor__(int(utils.to_value(value)))

    def __rlshift__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rlshift__(int(utils.to_value(value)))

    def __rrshift__(self, value: Union[int, IntProxy]) -> int:
        return self._ref.value.__rrshift__(int(utils.to_value(value)))

    def __neg__(self) -> int:
        return self._ref.value.__neg__()

    def __pos__(self) -> int:
        return self._ref.value.__pos__()

    def __invert__(self) -> int:
        return self._ref.value.__invert__()

    def __trunc__(self) -> int:
        return self._ref.value.__trunc__()

    def __ceil__(self) -> int:
        return self._ref.value.__ceil__()

    def __floor__(self) -> int:
        return self._ref.value.__floor__()

    def __round__(self, ndigits: SupportsIndex = 0) -> int:
        return self._ref.value.__round__(ndigits)

    def __getnewargs__(self) -> Tuple[int]:
        return self._ref.value.__getnewargs__()

    def __eq__(self, value: object) -> bool:
        return self._ref.value.__eq__(int(utils.to_value(value)))

    def __ne__(self, value: object) -> bool:
        return self._ref.value.__ne__(int(utils.to_value(value)))

    def __lt__(self, value) -> bool:
        return self._ref.value.__lt__(int(utils.to_value(value)))

    def __le__(self, value) -> bool:
        return self._ref.value.__le__(int(utils.to_value(value)))

    def __gt__(self, value) -> bool:
        return self._ref.value.__gt__(int(utils.to_value(value)))

    def __ge__(self, value) -> bool:
        return self._ref.value.__ge__(int(utils.to_value(value)))

    def __float__(self) -> float:
        return self._ref.value.__float__()

    def __int__(self) -> int:
        return self._ref.value.__int__()

    def __abs__(self) -> int:
        return self._ref.value.__abs__()

    def __hash__(self) -> int:
        return self._ref.value.__hash__()

    def __bool__(self) -> bool:
        return self._ref.value.__bool__()

    def __index__(self) -> int:
        return self._ref.value.__index__()
