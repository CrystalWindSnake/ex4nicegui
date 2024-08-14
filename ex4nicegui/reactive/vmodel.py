from __future__ import annotations
import inspect
from io import BytesIO
from ex4nicegui.utils.signals import (
    RefWrapper,
    TRef,
    to_raw,
    is_setter_ref,
    to_ref_wrapper,
    to_value,
    is_reactive,
)
from typing import (
    Any,
    Callable,
    TypeVar,
    Union,
    cast,
    Tuple,
    NamedTuple,
)

from types import FrameType
import tokenize
import executing
import ast
import warnings
from ex4nicegui.reactive.systems.object_system import get_attribute, set_attribute
from ex4nicegui.utils.types import _TMaybeRef as TMaybeRef, Ref
from ex4nicegui.utils.signals import is_reactive

_T = TypeVar("_T")


def get_caller() -> FrameType:
    return inspect.currentframe().f_back.f_back  # type: ignore


def get_args_code(caller: FrameType) -> str:
    node = executing.Source.executing(caller).node

    assert isinstance(node, ast.Call)

    source = inspect.getsource(inspect.getmodule(caller))  # type: ignore
    key_code = ast.get_source_segment(source, node.args[0])
    return key_code  # type: ignore


class CodeInfo(NamedTuple):
    model: str
    is_ref: bool
    keys: Tuple[Union[str, int], ...] = tuple()  # type: ignore


def normalize(token: tokenize.TokenInfo):
    if token.type == tokenize.NUMBER:
        return int(token.string)

    if token.type == tokenize.STRING:
        return token.string[1:-1]

    return token.string


def parse_code(code: str) -> CodeInfo:
    tokens = [
        t
        for t in tokenize.tokenize(BytesIO(code.encode("utf8")).readline)
        if t.type in (tokenize.NAME, tokenize.NUMBER, tokenize.OP, tokenize.STRING)
    ]

    model = tokens[0].string
    is_ref = (
        len(tokens) >= 3
        and tokens[1].type == tokenize.OP
        and tokens[1].string == "."
        and tokens[2].string == "value"
    )

    keys_search_start = 3 if is_ref else 1

    keys = tuple(
        normalize(token)
        for token in tokens[keys_search_start:]
        if token.type != tokenize.OP
    )

    return CodeInfo(model, is_ref, keys)


def create_writeable_wrapper(expr, ref_data, attrs: Tuple[Union[str, int], ...]):
    if not attrs:

        def maybe_ref_getter():
            return to_value(expr)

        def reactive_getter():
            return to_raw(expr)

        def setter(value):
            pass

        wrapper = to_ref_wrapper(
            reactive_getter if is_reactive(expr) else maybe_ref_getter,
            setter,
        )
        wrapper._is_readonly = False
        return wrapper

    def getter():
        obj = get_attribute(to_value(ref_data), attrs[0])
        for attr in attrs[1:]:
            obj = get_attribute(obj, attr)

        return obj

    def setter(value):
        obj = to_value(ref_data)

        for attr in attrs[:-1]:
            obj = get_attribute(obj, attr)

        set_attribute(obj, attrs[-1], value)

    wrapper = to_ref_wrapper(
        getter,
        setter,
    )
    wrapper._is_readonly = False
    return wrapper


def vmodel(expr: Any, *attrs: Union[str, int]) -> TRef[Any]:
    """Create a two-way binding on a form input element or a component.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#vmodel
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#vmodel

    Args:
        expr (Any): _description_

    ## Examples
    ```python
    from ex4nicegui.reactive import rxui
    from ex4nicegui import deep_ref

    data = deep_ref({"a": 1, "b": [1, 2, 3, 4]})

    rxui.label(lambda: f"{data.value=!s}")

    # No binding effect
    rxui.input(value=data.value["a"])

    # readonly binding
    rxui.input(value=lambda: data.value["a"])

    # two-way binding
    rxui.input(value=rxui.vmodel(data.value["a"]))
    ```

    """

    assert not isinstance(expr, Callable), "argument expr cannot be a function"

    if isinstance(expr, RefWrapper):
        expr._is_readonly = False

    if is_setter_ref(expr):
        if attrs:
            wrapper = create_writeable_wrapper(expr, expr, attrs)

            return cast(
                TRef,
                wrapper,
            )

        return cast(
            TRef,
            expr,
        )

    caller = get_caller()
    code = get_args_code(caller)

    info = parse_code(code)
    ref_data = caller.f_locals.get(info.model) or caller.f_globals.get(info.model)
    assert ref_data is not None, f"{info.model} not found"
    all_attrs = (*info.keys, *attrs)

    if not all_attrs:
        warn_mes = ""
        if is_reactive(expr) or is_setter_ref(expr):
            warn_mes = rf"""Expression missing the key,result is read-only binding.Maybe you meant `{code}['key']`"""
        elif not info.is_ref:
            warn_mes = """Maybe you don't need to use vmodel"""
        else:
            warn_mes = rf"""No binding.Maybe you meant `{info.model}`"""

        warnings.warn(
            warn_mes,
            stacklevel=2,
        )

    wrapper = create_writeable_wrapper(expr, ref_data, all_attrs)

    return cast(
        TRef,
        wrapper,
    )


# def _get_item(obj, key):
#     if isinstance(key, (list, dict)):
#         return obj[key]
#     else:
#         return getattr(obj, key)


# def _set_item(obj, key, value):
#     if isinstance(key, (list, dict)):
#         obj[key] = value
#     else:
#         setattr(obj, key, value)


# def vmodel(ref: Ref, *keys: Union[str, int]) -> Ref:
#     item = ref if is_reactive(ref) else ref.value

#     def getter():
#         result = item

#         for k in keys:
#             result = get_attribute(result, k)
#         return result

#     def setter(value):
#         if len(keys) == 1:
#             set_attribute(item, keys[0], value)
#             return

#         obj = get_attribute(item, keys[0])

#         for k in keys[1:-1]:
#             set_attribute(obj, k, get_attribute(obj, k))

#         set_attribute(obj, keys[-1], value)

#     return RefWrapper(getter, setter)  # type: ignore


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
