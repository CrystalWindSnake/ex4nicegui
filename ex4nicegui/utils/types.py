from __future__ import annotations
from typing import TypeVar, Callable, Any, Generic
from typing_extensions import ParamSpec, Concatenate, Protocol


T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


class Method(Protocol, Generic[P, R]):
    def __get__(self, instance: Any, owner: type | None = None) -> Callable[P, R]:
        ...

    def __call__(self_, self: Any, *args: P.args, **kwargs: P.kwargs) -> R:
        ...


# , "return": f.__annotations__["return"]
def mirror_method(x: Callable[P, Any]):
    def decorator(f: Callable[..., R]) -> Method[P, R]:
        f.__annotations__ = {**x.__annotations__}
        return f  # type: ignore

    return decorator


def mirror_func(x: Callable[P, Any]):
    def decorator(f: Callable[..., R]) -> Callable[P, R]:
        f.__annotations__ = {**x.__annotations__}
        return f  # type: ignore

    return decorator
