import typing
from typing_extensions import ParamSpec, Concatenate

P = ParamSpec("P")
R = typing.TypeVar("R")


def with_signature_from(
    f: typing.Callable[Concatenate[typing.Any, P], R],
) -> typing.Callable[
    [typing.Callable[Concatenate[typing.Any, P], R]],
    typing.Callable[Concatenate[typing.Any, P], R],
]:
    return lambda _: _
