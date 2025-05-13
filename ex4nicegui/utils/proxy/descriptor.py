import sys
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Generic
from .base import ProxyProtocol
from .int import IntProxy
from .list import ListProxy
from .string import StringProxy
from .float import FloatProxy
from .bool import BoolProxy
from .date import DateProxy
from .dict import DictProxy
from ex4nicegui.utils.signals import deep_ref
import datetime
import warnings
from . import to_value_if_base_type_proxy

T = TypeVar("T")


class ProxyDescriptor(Generic[T]):
    def __init__(
        self,
        name: str,
        value: T,
        proxy_builder: Callable[[T], ProxyProtocol],
        proxy_rebuilder: Optional[Callable[[ProxyProtocol], ProxyProtocol]] = None,
    ) -> None:
        self.value = value
        self.name = name
        self._proxy_builder = proxy_builder
        self._proxy_rebuilder = proxy_rebuilder

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._proxy_builder(self.value)
            instance.__dict__[self.name] = proxy
        else:
            proxy = self._proxy_rebuilder(proxy) if self._proxy_rebuilder else proxy
        proxy._ref.value  # type: ignore
        return proxy

    def __set__(self, instance: object, value: T) -> None:
        value = to_value_if_base_type_proxy(value)
        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._proxy_builder(value)  # type: ignore
            instance.__dict__[self.name] = proxy

        proxy._ref.value = value  # type: ignore


class IntDescriptor(ProxyDescriptor[int]):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value, IntProxy)


class ListDescriptor(ProxyDescriptor[Callable[[], List]]):
    def __init__(self, name: str, value: Callable[[], List]) -> None:
        super().__init__(name, value, lambda x: ListProxy(x() if callable(x) else x))


class DictDescriptor:
    def __init__(
        self,
        name: str,
        factory: Callable[[], Dict],
    ) -> None:
        self.name = name
        self._ref_builder = lambda: deep_ref(factory())

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._ref_builder()
            instance.__dict__[self.name] = proxy

        return proxy.value

    def __set__(self, instance: object, value: T) -> None:
        value = to_value_if_base_type_proxy(value)
        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._ref_builder()
            instance.__dict__[self.name] = proxy

        proxy.value = value  # type: ignore


class StringDescriptor(ProxyDescriptor[str]):
    def __init__(self, name: str, value: str) -> None:
        def rebuild_proxy(proxy: ProxyProtocol) -> ProxyProtocol:
            sp = StringProxy(proxy._ref.value)
            sp._ref = proxy._ref
            return sp

        super().__init__(name, value, StringProxy, rebuild_proxy)


class FloatDescriptor(ProxyDescriptor[float]):
    def __init__(self, name: str, value: float) -> None:
        super().__init__(name, value, FloatProxy)


class BoolDescriptor(ProxyDescriptor[bool]):
    def __init__(self, name: str, value: bool) -> None:
        super().__init__(name, value, BoolProxy)


class DateDescriptor(ProxyDescriptor[datetime.date]):
    def __init__(self, name: str, value: datetime.date) -> None:
        super().__init__(name, value, lambda x: DateProxy(x.year, x.month, x.day))


def class_var_setter(
    cls: Type, name: str, value, list_var_flat: str, dict_var_flat: str
) -> None:
    if value is None or isinstance(value, str):
        setattr(cls, name, StringDescriptor(name, value))
    elif isinstance(value, bool):
        setattr(cls, name, BoolDescriptor(name, value))
    elif isinstance(value, int):
        setattr(cls, name, IntDescriptor(name, value))
    elif callable(value) and hasattr(value, list_var_flat):
        setattr(cls, name, ListDescriptor(name, value))

    elif isinstance(value, list):
        if len(value) > 0:
            with warnings.catch_warnings():
                warnings.showwarning = _custom_showwarning
                warnings.warn(
                    f"The variable [{cls.__name__}.{name}] will be empty list.you should initialize it in the constructor,or use list_var for definition.\n {name} = rxui.list_var(lambda:[1,2,3])",
                    stacklevel=3,
                )
        setattr(cls, name, ListDescriptor(name, lambda: []))

    elif callable(value) and hasattr(value, dict_var_flat):
        setattr(cls, name, DictDescriptor(name, value))
    elif isinstance(value, float):
        setattr(cls, name, FloatDescriptor(name, value))
    elif isinstance(value, datetime.date):
        setattr(cls, name, DateDescriptor(name, value))
    else:
        pass


def _custom_showwarning(message, category, filename, lineno, file=None, line=None):
    sys.stderr.write(f"{filename}:{lineno}: {category.__name__}: {message}\n")
