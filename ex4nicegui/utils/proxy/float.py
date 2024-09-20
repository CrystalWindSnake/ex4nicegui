import sys
from typing import Any, Optional, SupportsIndex, Tuple, overload
from . import utils


class FloatProxy:
    # def __new__(cls, value):
    #     return super().__new__(cls, value)

    def __init__(self, value: float):
        from ex4nicegui.utils.signals import to_ref

        self._ref = to_ref(value)

    def __str__(self) -> str:
        return str(self._ref.value)

    def as_integer_ratio(self) -> Tuple[int, int]:
        return self._ref.value.as_integer_ratio()

    def hex(self) -> str:
        return self._ref.value.hex()

    def is_integer(self) -> bool:
        return self._ref.value.is_integer()

    @property
    def real(self) -> float:
        return self._ref.value.real

    @property
    def imag(self) -> float:
        return self._ref.value.imag

    def conjugate(self) -> float:
        return self._ref.value.conjugate()

    def __add__(self, value: float, /) -> float:
        return self._ref.value.__add__(float(utils.to_value(value)))

    def __sub__(self, value: float, /) -> float:
        return self._ref.value.__sub__(float(utils.to_value(value)))

    def __mul__(self, value: float, /) -> float:
        return self._ref.value.__mul__(float(utils.to_value(value)))

    def __floordiv__(self, value: float, /) -> float:
        return self._ref.value.__floordiv__(float(utils.to_value(value)))

    def __truediv__(self, value: float, /) -> float:
        return self._ref.value.__truediv__(float(utils.to_value(value)))

    def __mod__(self, value: float, /) -> float:
        return self._ref.value.__mod__(float(utils.to_value(value)))

    def __divmod__(self, value: float, /) -> Tuple[float, float]:
        return self._ref.value.__divmod__(float(utils.to_value(value)))

    @overload
    def __pow__(self, value: int, mod: None = None, /) -> float: ...
    # positive __value -> float; negative __value -> complex
    # return type must be Any as `float | complex` causes too many false-positive errors
    @overload
    def __pow__(self, value: float, mod: None = None, /) -> Any: ...

    def __pow__(self, value: float, mod: None = None, /) -> Any:
        return self._ref.value.__pow__(float(utils.to_value(value)), mod)

    def __radd__(self, value: float, /) -> float:
        return self._ref.value.__radd__(float(utils.to_value(value)))

    def __rsub__(self, value: float, /) -> float:
        return self._ref.value.__rsub__(float(utils.to_value(value)))

    def __rmul__(self, value: float, /) -> float:
        return self._ref.value.__rmul__(float(utils.to_value(value)))

    def __rfloordiv__(self, value: float, /) -> float:
        return self._ref.value.__rfloordiv__(float(utils.to_value(value)))

    def __rtruediv__(self, value: float, /) -> float:
        return self._ref.value.__rtruediv__(float(utils.to_value(value)))

    def __rmod__(self, value: float, /) -> float:
        return self._ref.value.__rmod__(float(utils.to_value(value)))

    def __rdivmod__(self, value: float, /) -> Tuple[float, float]:
        return self._ref.value.__rdivmod__(float(utils.to_value(value)))

    def __rpow__(self, value, mod: None = None, /) -> float:
        return self._ref.value.__rpow__(float(utils.to_value(value)), mod)  # type: ignore

    def __getnewargs__(self) -> Tuple[float]:
        return (self._ref.value,)

    def __trunc__(self) -> int:
        return self._ref.value.__trunc__()

    if sys.version_info >= (3, 9):

        def __ceil__(self) -> int:
            return self._ref.value.__ceil__()

        def __floor__(self) -> int:
            return self._ref.value.__floor__()

    @overload
    def __round__(self, ndigits: None = None, /) -> int: ...
    @overload
    def __round__(self, ndigits: SupportsIndex, /) -> float: ...

    def __round__(self, ndigits: Optional[SupportsIndex] = None, /):
        return self._ref.value.__round__(ndigits)

    def __eq__(self, value: object, /) -> bool:
        return self._ref.value.__eq__(float(utils.to_value(value)))

    def __ne__(self, value: object, /) -> bool:
        return self._ref.value.__ne__(float(utils.to_value(value)))

    def __lt__(self, value: float, /) -> bool:
        return self._ref.value.__lt__(float(utils.to_value(value)))

    def __le__(self, value: float, /) -> bool:
        return self._ref.value.__le__(float(utils.to_value(value)))

    def __gt__(self, value: float, /) -> bool:
        return self._ref.value.__gt__(float(utils.to_value(value)))

    def __ge__(self, value: float, /) -> bool:
        return self._ref.value.__ge__(float(utils.to_value(value)))

    def __neg__(self) -> float:
        return self._ref.value.__neg__()

    def __pos__(self) -> float:
        return self._ref.value.__pos__()

    def __int__(self) -> int:
        return self._ref.value.__int__()

    def __float__(self) -> float:
        return self._ref.value.__float__()

    def __abs__(self) -> float:
        return self._ref.value.__abs__()

    def __hash__(self) -> int:
        return self._ref.value.__hash__()

    def __bool__(self) -> bool:
        return self._ref.value.__bool__()
