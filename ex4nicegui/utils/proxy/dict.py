import sys
from typing import (
    Dict,
    Iterator,
    TypeVar,
)
import datetime
from .string import StringProxy
from .int import IntProxy
from .float import FloatProxy
from .bool import BoolProxy
from .date import DateProxy

from signe import to_raw
from ex4nicegui.utils.signals import to_ref_wrapper

from weakref import WeakValueDictionary

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DictProxy(dict[_KT, _VT]):
    def __init__(self, value: Dict):
        from ex4nicegui.utils.signals import deep_ref

        super().__init__(value)
        self._ref = deep_ref(value)

        self.__key_cache = {}

    def copy(self) -> dict[_KT, _VT]:
        return to_raw(self._ref.value).copy()

    def keys(self):
        return to_raw(self._ref.value).keys()

    def values(self):
        return to_raw(self._ref.value).values()

    def items(self):
        # print("items")
        # return ((k, self[k]) for k in self.keys())
        return to_raw(self._ref.value).items()

    def get(self, key: _KT, default, /):
        return self._ref.value.get(key, default)

    def pop(self, key: _KT, default, /):
        return self._ref.value.pop(key, default)

    def __len__(self) -> int:
        return self._ref.value.__len__()

    def __getitem__(self, key: _KT, /):
        print("getitem")
        value = self._ref.value.__getitem__(key)

        if isinstance(value, str):
            if key not in self.__key_cache:
                self.__key_cache[key] = StringProxy(value)

            sp = self.__key_cache[key]

            def getter():
                return to_raw(self._ref.value)[key]

            def setter(v):
                self._ref.value[key] = v

            sp._ref = to_ref_wrapper(getter, setter)

            return sp
        elif isinstance(value, int):
            return IntProxy(value)
        elif isinstance(value, float):
            return FloatProxy(value)
        elif isinstance(value, bool):
            return BoolProxy(value)
        elif isinstance(value, datetime.date):
            return DateProxy(value.year, value.month, value.day)
        else:
            pass

        return value

    def __setitem__(self, key: _KT, value: _VT, /) -> None:
        self._ref.value.__setitem__(key, value)

    def __delitem__(self, key: _KT, /) -> None:
        self._ref.value.__delitem__(key)

    def __iter__(self) -> Iterator[_KT]:
        return self._ref.value.__iter__()

    def __eq__(self, value: object, /) -> bool:
        return self._ref.value.__eq__(value)

    def __reversed__(self) -> Iterator[_KT]:
        return self._ref.value.__reversed__()

    def __str__(self) -> str:
        return self._ref.value.__str__()

    def __contains__(self, key: object) -> bool:
        return self._ref.value.__contains__(key)

    if sys.version_info >= (3, 9):

        def __or__(self, value, /):
            return self._ref.value.__or__(value)

        def __ror__(self, value, /):
            return self._ref.value.__ror__(value)

        def __ior__(self, value, /):
            self._ref.value.update(value)
