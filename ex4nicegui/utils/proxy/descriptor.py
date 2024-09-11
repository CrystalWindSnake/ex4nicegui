from typing import Any, Callable, List, Type, TypeVar, Generic
from .base import ProxyProtocol
from .int import IntProxy
from .list import ListProxy
from .string import StringProxy
from .float import FloatProxy

T = TypeVar("T")


class ProxyDescriptor(Generic[T]):
    def __init__(
        self, name: str, value: T, proxy_builder: Callable[[T], ProxyProtocol]
    ) -> None:
        self.value = value
        self.name = name
        self._proxy_builder = proxy_builder

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._proxy_builder(self.value)
            instance.__dict__[self.name] = proxy
        proxy._ref.value  # type: ignore
        return proxy

    def __set__(self, instance: object, value: T) -> None:
        proxy = instance.__dict__.get(self.name, None)
        if proxy is None:
            proxy = self._proxy_builder(value)
            instance.__dict__[self.name] = proxy

        proxy._ref.value = value  # type: ignore


class IntDescriptor(ProxyDescriptor[int]):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value, IntProxy)


class ListDescriptor(ProxyDescriptor[List]):
    def __init__(self, name: str, value: List) -> None:
        super().__init__(name, value, ListProxy)


class StringDescriptor(ProxyDescriptor[str]):
    def __init__(self, name: str, value: str) -> None:
        super().__init__(name, value, StringProxy)


class FloatDescriptor(ProxyDescriptor[float]):
    def __init__(self, name: str, value: float) -> None:
        super().__init__(name, value, FloatProxy)


def class_var_setter(cls: Type, name: str, value) -> None:
    if isinstance(value, str):
        setattr(cls, name, StringDescriptor(name, value))
    elif isinstance(value, int):
        setattr(cls, name, IntDescriptor(name, value))
    elif isinstance(value, list):
        setattr(cls, name, ListDescriptor(name, value))
    elif isinstance(value, float):
        setattr(cls, name, FloatDescriptor(name, value))
    else:
        pass
