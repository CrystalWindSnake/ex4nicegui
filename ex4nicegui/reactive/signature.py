from typing import Any, Callable, List, Optional, cast
from typing_extensions import Literal
from nicegui import ui


def select(
    label: Optional[str] = None,
    value: Any = None,
    on_change: Optional[Callable[..., Any]] = None,
    with_input: bool = False,
    multiple: bool = False,
    clearable: bool = False,
):
    ...


Table_Defalut_pagination = 10


def table(
    row_key: str = "id",
    title: Optional[str] = None,
    selection: Optional[Literal["single", "multiple"]] = None,
    pagination: Optional[int] = Table_Defalut_pagination,
    on_select: Optional[Callable[..., Any]] = None,
):
    pass


def aggrid(*, html_columns: List[int] = [], theme: str = "balham"):
    pass


def echarts(*, on_change: Optional[Callable] = None):
    pass
