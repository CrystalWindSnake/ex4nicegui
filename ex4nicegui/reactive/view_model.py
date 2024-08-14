from __future__ import annotations
from typing import Callable, Union, Type, TypeVar
from ex4nicegui.utils.signals import (
    deep_ref,
    is_ref,
    to_value,
    to_ref,
    on,
    to_raw,
    ref_computed as computed,
    Ref,
)


class ViewModel:
    def __init__(self):
        for name, value in self.__class__.__dict__.items():
            if is_ref(value):
                setattr(self, name, deep_ref(to_value(value)))

        for name, value in self.__dict__.items():
            if callable(value) and hasattr(value, "__vm_cached__"):
                setattr(self, name, computed(value))

    @staticmethod
    def display(model: Union[ViewModel, Type]):
        result = to_ref("")

        watch_refs = recursive_to_refs(model)

        all_refs = {
            key: value for key, value in model.__dict__.items() if is_ref(value)
        }

        @on(watch_refs)
        def _():
            result.value = str(
                {key: recursive_to_value(value) for key, value in all_refs.items()}
            )

        return result


def recursive_to_value(value_or_model):
    value = to_raw(to_value(value_or_model))

    if isinstance(value, ViewModel):
        all_refs = {
            key: value for key, value in value.__dict__.items() if is_ref(value)
        }
        return {key: recursive_to_value(value) for key, value in all_refs.items()}
    elif isinstance(value, dict):
        return {key: recursive_to_value(val) for key, val in value.items()}
    elif isinstance(value, list):
        return [recursive_to_value(val) for val in value]
    else:
        return value


def recursive_to_refs(model):
    result = []
    stack = [model]

    def handle_ref(value):
        if is_ref(value):
            stack.append(value.value)
            result.append(value)

        elif isinstance(value, (ViewModel, Type)):
            stack.append(value)
        elif isinstance(value, dict):
            stack.append(value)

    while stack:
        current = stack.pop()

        if isinstance(current, (ViewModel, Type)):
            for key, value in current.__dict__.items():
                handle_ref(value)

        elif isinstance(current, dict):
            for key, value in current.items():
                handle_ref(value)

        elif isinstance(current, list):
            for value in current:
                handle_ref(value)

    return result


_T_Var_Value = TypeVar("_T_Var_Value")


def var(value: Union[_T_Var_Value, Callable[[], _T_Var_Value]]) -> Ref[_T_Var_Value]:
    if callable(value):
        return deep_ref(value())
    return deep_ref(value)


def cached_var(func: Callable):
    func.__vm_cached__ = True
    return func
