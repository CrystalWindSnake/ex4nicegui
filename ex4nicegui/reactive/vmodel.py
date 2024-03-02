from __future__ import annotations
import inspect
from io import BytesIO
from ex4nicegui.utils.signals import (
    RefWrapper,
    TRef,
    is_setter_ref,
    to_ref_wrapper,
    to_value,
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
from .utils import get_attribute, set_attribute

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


def create_writeable_wrapper(ref, attrs: Tuple[Union[str, int], ...]):
    def getter():
        obj = get_attribute(to_value(ref), attrs[0])
        for attr in attrs[1:]:
            obj = get_attribute(obj, attr)

        return obj

    def setter(value):
        obj = to_value(ref)

        for attr in attrs[:-1]:
            obj = get_attribute(obj, attr)

        set_attribute(obj, attrs[-1], value)

    wrapper = to_ref_wrapper(
        getter,
        setter,
    )
    wrapper._is_readonly = False
    return wrapper


def vmodel(ref: Any, *attrs: Union[str, int]) -> TRef[Any]:
    """Create a two-way binding on a form input element or a component.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#vmodel
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#vmodel

    Args:
        ref (Any): _description_

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

    assert not isinstance(ref, Callable), "Functions cannot be passed as arguments ref"

    if isinstance(ref, RefWrapper):
        ref._is_readonly = False

    if is_setter_ref(ref):
        if attrs:
            wrapper = create_writeable_wrapper(ref, attrs)

            return cast(
                TRef,
                wrapper,
            )

        return cast(
            TRef,
            ref,
        )

    caller = get_caller()
    code = get_args_code(caller)

    info = parse_code(code)
    ref_data = caller.f_locals.get(info.model) or caller.f_globals.get(info.model)
    assert ref_data is not None, f"{info.model} not found"

    wrapper = create_writeable_wrapper(ref_data, (*info.keys, *attrs))

    return cast(
        TRef,
        wrapper,
    )
