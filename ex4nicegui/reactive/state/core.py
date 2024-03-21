from __future__ import annotations
import inspect
from typing import Callable, Tuple

from ex4nicegui.utils.signals import deep_ref
from weakref import WeakValueDictionary


from ex4nicegui.utils.signals import (
    TRef,
)


class RefDescriptor:
    def __init__(self, value) -> None:
        self._init_value = value
        self._instance_map: WeakValueDictionary[
            Tuple[object, RefDescriptor], TRef
        ] = WeakValueDictionary()

    def __get__(self, obj, objtype=None):
        if not obj:
            return

        key = (self, obj)
        ref = self._instance_map.get(key)
        if not ref:
            ref = deep_ref(self._init_value)
            self._instance_map[key] = ref

        if obj._rendering and obj._frame_id == id(inspect.currentframe().f_back.f_back):  # type: ignore
            return ref

        return ref.value

    def __set__(self, obj, value):
        if not obj:
            return

        key = (self, obj)
        ref = self._instance_map.get(key)
        assert ref
        ref.value = value


class PropertyDescriptor:
    def __init__(self, prop) -> None:
        self._prop: property = prop

    def __get__(self, obj, objtype=None):
        if not obj:
            return

        if obj._rendering and obj._frame_id == id(inspect.currentframe().f_back.f_back):  # type: ignore
            return lambda: self._prop.fget(obj)  # type: ignore

        return self._prop.fget(obj)  # type: ignore


class RefState:
    def __init__(self) -> None:
        self._rendering = False
        self._frame_id = 0

    def __init_subclass__(cls) -> None:
        for attr, value in RefState.class_vars(cls):
            setattr(cls, attr, RefDescriptor(value))

        for attr, value in RefState.class_props(cls):
            setattr(cls, attr, PropertyDescriptor(value))

        if hasattr(cls, "view"):
            view_fn = getattr(cls, "view")
            if isinstance(view_fn, Callable):

                def wrap_view(
                    self,
                ):
                    self._rendering = True
                    self._frame_id = id(inspect.currentframe())
                    try:
                        view_fn(self)
                    finally:
                        self._rendering = False

                setattr(cls, "view", wrap_view)

    @staticmethod
    def class_vars(child):
        return [
            (name, value)
            for name, value in vars(child).items()
            if name[0] != "_" and not isinstance(value, (Callable, property))
        ]

    @staticmethod
    def class_props(child):
        return [
            (name, value)
            for name, value in vars(child).items()
            if name[0] != "_" and isinstance(value, (property))
        ]
