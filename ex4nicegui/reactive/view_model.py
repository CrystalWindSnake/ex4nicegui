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
from functools import partial

_CACHED_VARS_FLAG = "__vm_cached__"


class ViewModel:
    """A base class for reactive view models.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#ViewModel

    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#ViewModel

    Example:
    .. code-block:: python
        from ex4nicegui import rxui

        class MyVm(rxui.ViewModel):
            count = rxui.var(0)
            data = rxui.var(lambda: [1,2,3])

        vm = MyVm()

        rxui.label(vm.count)
        rxui.number(value=vm.count)


    """

    def __init__(self):
        for name, value in self.__class__.__dict__.items():
            if is_ref(value):
                setattr(self, name, deep_ref(to_value(value)))
            if callable(value) and hasattr(value, _CACHED_VARS_FLAG):
                setattr(self, name, computed(partial(value, self)))

    @staticmethod
    def display(model: Union[ViewModel, Type]):
        result = to_ref("")

        watch_refs = _recursive_to_refs(model)

        all_refs = {
            key: value for key, value in model.__dict__.items() if is_ref(value)
        }

        @on(watch_refs)
        def _():
            result.value = str(
                {key: _recursive_to_value(value) for key, value in all_refs.items()}
            )

        return result


def _recursive_to_value(value_or_model):
    value = to_raw(to_value(value_or_model))

    if isinstance(value, ViewModel):
        all_refs = {
            key: value for key, value in value.__dict__.items() if is_ref(value)
        }
        return {key: _recursive_to_value(value) for key, value in all_refs.items()}
    elif isinstance(value, dict):
        return {key: _recursive_to_value(val) for key, val in value.items()}
    elif isinstance(value, list):
        return [_recursive_to_value(val) for val in value]
    else:
        return value


def _recursive_to_refs(model):
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
    """Create a reactive variable. Only use within rxui.ViewModel.

    Args:
        value (Union[_T_Var_Value, Callable[[], _T_Var_Value]]): The initial value or a function to generate the initial value.

    Example:
    .. code-block:: python
        from ex4nicegui import rxui
        class MyVm(rxui.ViewModel):
            count = rxui.var(0)
            data = rxui.var(lambda: [1,2,3])


    """
    if callable(value):
        return deep_ref(value())
    return deep_ref(value)


def cached_var(func: Callable):
    """A decorator to cache the result of a function. Only use within rxui.ViewModel.

    Args:
        func (Callable): The function to cache.

    Example:
    .. code-block:: python
        from ex4nicegui import rxui
        class MyVm(rxui.ViewModel):
            name = rxui.var("John")

        @rxui.cached_var
        def uppper_name(self):
            return self.name.value.upper()

    """
    setattr(func, _CACHED_VARS_FLAG, None)
    return func
