from __future__ import annotations
import warnings
from ex4nicegui.utils.signals import (
    RefWrapper,
    TRef,
    to_raw,
    to_ref_wrapper,
    to_value,
    is_reactive,
    is_ref,
)
from typing import (
    Any,
    Union,
    cast,
    Tuple,
)

from ex4nicegui.reactive.systems.object_system import get_attribute, set_attribute
from ex4nicegui.utils.types import _TMaybeRef as TMaybeRef, Ref


def create_writeable_wrapper(ref_obj: TRef, attrs: Tuple[Union[str, int], ...]):
    if not attrs:

        def maybe_ref_getter():
            return to_value(ref_obj)

        def reactive_getter():
            return to_raw(ref_obj)

        def setter(value):
            pass

        wrapper = to_ref_wrapper(
            reactive_getter if is_reactive(ref_obj) else maybe_ref_getter,
            setter,
        )
        wrapper._is_readonly = False
        return wrapper

    def getter():
        obj = get_attribute(to_value(ref_obj), attrs[0])
        for attr in attrs[1:]:
            obj = get_attribute(obj, attr)

        return obj

    def setter(value):
        obj = to_value(ref_obj)

        for attr in attrs[:-1]:
            obj = get_attribute(obj, attr)

        set_attribute(obj, attrs[-1], value)

    wrapper = to_ref_wrapper(
        getter,
        setter,
    )
    wrapper._is_readonly = False
    return wrapper


def vmodel(ref_obj: Union[TRef[Any], Any], *attrs: Union[str, int]) -> Any:
    """Create a two-way binding on a form input element or a component.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#vmodel
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#vmodel

    Args:
        expr (Any): _description_

    ## Examples

    .. code-block:: python
        from ex4nicegui.reactive import rxui
        from ex4nicegui import deep_ref

        data = deep_ref({"a": 1, "b": [1, 2, 3, 4]})

        rxui.label(lambda: f"{data.value=!s}")

        # No binding effect
        rxui.input(value=data.value["a"])

        # readonly binding
        rxui.input(value=lambda: data.value["a"])

        # two-way binding
        rxui.input(value=rxui.vmodel(data.value,'a'))


    """

    if not is_ref(ref_obj):
        result = cast(Any, ref_obj)
        for attr in attrs:
            result = result[attr]

        return result

    if isinstance(ref_obj, RefWrapper):
        ref_obj._is_readonly = False

    if attrs:
        wrapper = create_writeable_wrapper(ref_obj, attrs)

        return cast(
            TRef,
            wrapper,
        )
    else:
        warnings.warn(
            """Maybe you don't need to use vmodel""",
            stacklevel=2,
        )

    return cast(
        TRef,
        ref_obj,
    )


def vmodel_with_index(ref: Ref, index: TMaybeRef[int], *keys: Union[str, int]) -> Ref:
    proxy = ref.value

    def getter():
        item = proxy[to_value(index)]
        result = item

        for k in keys:
            result = get_attribute(result, k)
        return result

    def setter(value):
        item = proxy[to_value(index)]

        if len(keys) == 1:
            set_attribute(item, keys[0], value)
            return

        obj = get_attribute(item, keys[0])

        for k in keys[1:-1]:
            set_attribute(obj, k, get_attribute(obj, k))

        set_attribute(obj, keys[-1], value)

    return RefWrapper(getter, setter)  # type: ignore
