from typing import (
    Any,
    Literal,
    Optional,
    SupportsIndex,
    Tuple,
    Union,
)
import sys
from ex4nicegui.utils.signals import to_ref


class IntProxy(int):
    def __new__(cls, value):
        return super().__new__(cls, value)

    def __init__(self, value: int):
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

    def __add__(self, value: int) -> int:
        return self._ref.value.__add__(value)

    def __sub__(self, value: int) -> int:
        return self._ref.value.__sub__(value)

    def __mul__(self, value: int) -> int:
        return self._ref.value.__mul__(value)

    def __floordiv__(self, value: int) -> int:
        return self._ref.value.__floordiv__(value)

    def __truediv__(self, value: int) -> float:
        return self._ref.value.__truediv__(value)

    def __mod__(self, value: int) -> int:
        return self._ref.value.__mod__(value)

    def __divmod__(self, value: int) -> Tuple[int, int]:
        return self._ref.value.__divmod__(value)

    def __radd__(self, value: int) -> int:
        return self._ref.value.__radd__(value)

    def __rsub__(self, value: int) -> int:
        return self._ref.value.__rsub__(value)

    def __rmul__(self, value: int) -> int:
        return self._ref.value.__rmul__(value)

    def __rfloordiv__(self, value: int) -> int:
        return self._ref.value.__rfloordiv__(value)

    def __rtruediv__(self, value: int) -> float:
        return self._ref.value.__rtruediv__(value)

    def __rmod__(self, value: int) -> int:
        return self._ref.value.__rmod__(value)

    def __rdivmod__(self, value: int) -> Tuple[int, int]:
        return self._ref.value.__rdivmod__(value)

    def __pow__(self, value: int, mod: Optional[int] = None) -> Union[int, float]:
        return self._ref.value.__pow__(value, mod)

    def __rpow__(self, value: int, mod: Optional[int] = None) -> Union[int, float]:
        return self._ref.value.__rpow__(value, mod)

    def __and__(self, value: int) -> int:
        return self._ref.value.__and__(value)

    def __or__(self, value: int) -> int:
        return self._ref.value.__or__(value)

    def __xor__(self, value: int) -> int:
        return self._ref.value.__xor__(value)

    def __lshift__(self, value: int) -> int:
        return self._ref.value.__lshift__(value)

    def __rshift__(self, value: int) -> int:
        return self._ref.value.__rshift__(value)

    def __rand__(self, value: int) -> int:
        return self._ref.value.__rand__(value)

    def __ror__(self, value: int) -> int:
        return self._ref.value.__ror__(value)

    def __rxor__(self, value: int) -> int:
        return self._ref.value.__rxor__(value)

    def __rlshift__(self, value: int) -> int:
        return self._ref.value.__rlshift__(value)

    def __rrshift__(self, value: int) -> int:
        return self._ref.value.__rrshift__(value)

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
        return self._ref.value.__eq__(value)

    def __ne__(self, value: object) -> bool:
        return self._ref.value.__ne__(value)

    def __lt__(self, value: int) -> bool:
        return self._ref.value.__lt__(value)

    def __le__(self, value: int) -> bool:
        return self._ref.value.__le__(value)

    def __gt__(self, value: int) -> bool:
        return self._ref.value.__gt__(value)

    def __ge__(self, value: int) -> bool:
        return self._ref.value.__ge__(value)

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


class IntDescriptor:
    def __init__(self, name: str, value: int) -> None:
        self.value = value
        self.name = name

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = IntProxy(self.value)
            instance.__dict__[self.name] = proxy

        return proxy

    def __set__(self, instance: object, value: int) -> None:
        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = IntProxy(self.value)
            instance.__dict__[self.name] = proxy

        proxy._ref.value = value
