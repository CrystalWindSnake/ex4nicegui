from typing import (
    Any,
    Protocol,
    runtime_checkable,
    Union,
)


@runtime_checkable
class GetItemProtocol(Protocol):
    def __getitem__(self, key): ...


@runtime_checkable
class SetItemProtocol(Protocol):
    def __setitem__(self, key, value): ...


def get_attribute(obj: Union[object, GetItemProtocol], name: Union[str, int]) -> Any:
    if isinstance(obj, (GetItemProtocol)):
        return obj[name]
    return getattr(obj, name)  # type: ignore


def set_attribute(
    obj: Union[object, SetItemProtocol], name: Union[str, int], value: Any
) -> None:
    if isinstance(obj, SetItemProtocol):
        obj[name] = value
    else:
        setattr(obj, name, value)  # type: ignore
