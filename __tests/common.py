import typing
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = typing.TypeVar("R")


def with_signature_from(
    f: typing.Callable[typing.Concatenate[typing.Any, P], R],
) -> typing.Callable[
    [typing.Callable[typing.Concatenate[typing.Any, P], R]],
    typing.Callable[typing.Concatenate[typing.Any, P], R],
]:
    return lambda _: _
