from __future__ import annotations
from typing import Callable, Dict, Literal, TypeVar
from typing import TYPE_CHECKING


_TData = TypeVar("_TData")

_TElementID = int
_TNgClientID = str
_TFilterCallback = Callable[[_TData], _TData]

_TDataSourceId = int
_TSourceBuildFn = Callable[..., _TData]


_TDuplicates_column_values_sort_options = Dict[str, Literal["asc", "desc"]]
