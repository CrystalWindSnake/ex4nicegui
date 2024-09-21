from typing import Tuple
from . import utils


class BoolProxy:
    def __init__(self, value: bool):
        from ex4nicegui.utils.signals import to_ref

        if isinstance(value, (bool, int)):
            self._ref = to_ref(value)
        else:
            raise ValueError("only accepts boolean or integer values")

    def __bool__(self):
        return self._ref.value

    def __str__(self):
        return str(self._ref.value)

    def __eq__(self, other):
        return self._ref.value.__eq__(utils.to_value(other))

    def __ne__(self, other):
        return self._ref.value.__ne__(utils.to_value(other))

    def __lt__(self, value) -> bool:
        return self._ref.value.__lt__(bool(utils.to_value(value)))

    def __le__(self, value) -> bool:
        return self._ref.value.__le__(bool(utils.to_value(value)))

    def __gt__(self, value) -> bool:
        return self._ref.value.__gt__(bool(utils.to_value(value)))

    def __ge__(self, value) -> bool:
        return self._ref.value.__ge__(bool(utils.to_value(value)))

    def __and__(self, other):
        return self._ref.value.__and__(utils.to_value(other))

    def __or__(self, other):
        return self._ref.value.__or__(utils.to_value(other))

    def __xor__(self, other):
        return self._ref.value.__xor__(utils.to_value(other))

    def __rand__(self, value: bool, /) -> bool:
        return self._ref.value.__rand__(value)

    def __ror__(self, value: bool, /) -> bool:
        return self._ref.value.__ror__(value)

    def __rxor__(self, value: bool, /) -> bool:
        return self._ref.value.__rxor__(value)

    def __getnewargs__(self) -> Tuple[int]:
        return (int(self._ref.value),)
