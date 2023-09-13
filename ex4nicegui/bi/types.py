from typing import Callable, TypeVar


_TData = TypeVar("_TData")

_TElementID = int
_TComponentUpdateCallback = Callable[[_TData], None]
_TFilterCallback = Callable[[_TData], _TData]

_TDataSourceId = int
_TSourceBuildFn = Callable[..., _TData]
