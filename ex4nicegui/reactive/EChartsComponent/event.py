from typing import (
    Any,
    Optional,
)
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import (
    UiEventArguments,
)


@dataclass(**KWONLY_SLOTS)
class EChartsMouseEventArguments(UiEventArguments):
    componentType: str
    seriesType: str
    seriesIndex: int
    seriesName: str
    name: str
    dataIndex: int
    data: dict
    dataType: Optional[str]
    value: Any
    color: str
