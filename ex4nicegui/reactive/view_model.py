from __future__ import annotations
from typing import Callable, List, Union, Type, TypeVar
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
from ex4nicegui.utils.types import ReadonlyRef
from functools import partial
from signe.core.reactive import NoProxy
from ex4nicegui.utils.proxy.descriptor import class_var_setter


_CACHED_VARS_FLAG = "__vm_cached__"
_LIST_VAR_FLAG = "__vm_list_var__"

_T = TypeVar("_T")


class ViewModel(NoProxy):
    """A base class for reactive view models.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#ViewModel

    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#viewmodel

    Example:
    .. code-block:: python
        from ex4nicegui import rxui

        class MyVm(rxui.ViewModel):
            count = 0
            data = []
            nums = rxui.list_var(lambda: [1, 2, 3])

            def __init__(self):
                super().__init__()
                self.data = [1, 2, 3]

            def increment(self):
                self.count += 1

            def add_data(self):
                self.data.append(4)


        vm = MyVm()

        rxui.label(vm.count)
        rxui.number(value=vm.count)

        ui.button("Increment", on_click=vm.increment)
        ui.button("Add Data", on_click=vm.add_data)
        rxui.label(vm.data)
        rxui.label(vm.nums)
    """

    def __init__(self):
        for name, value in self.__class__.__dict__.items():
            if is_ref(value):
                setattr(self, name, deep_ref(to_value(value)))
            if callable(value) and hasattr(value, _CACHED_VARS_FLAG):
                setattr(self, name, computed(partial(value, self)))

    def __init_subclass__(cls) -> None:
        need_vars = (
            (name, value)
            for name, value in vars(cls).items()
            if not name.startswith("_")
        )

        for name, value in need_vars:
            class_var_setter(cls, name, value, _LIST_VAR_FLAG)

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


def list_var(factory: Callable[[], List[_T_Var_Value]]) -> List[_T_Var_Value]:
    """Create implicitly proxied reactive variables for lists. Use them just like ordinary lists while maintaining reactivity. Only use within rxui.ViewModel.

    Args:
        factory (Callable[[], List[_T_Var_Value]]): A factory function that returns a new list.

    Example:
    .. code-block:: python
        from ex4nicegui import rxui
        class State(rxui.ViewModel):
            data = rxui.list_var(lambda: [1, 2, 3])

            def append_data(self):
                self.data.append(len(self.data) + 1)

            def display_data(self):
                return ",".join(map(str, self.data))

        state = State()
        ui.button("Append", on_click=state.append_data)
        rxui.label(state.display_data)

    """
    assert callable(factory), "factory must be a callable"
    setattr(factory, _LIST_VAR_FLAG, None)
    return factory  # type: ignore


def cached_var(func: Callable[..., _T]) -> ReadonlyRef[_T]:
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
    return func  # type: ignore
