from typing import (
    Any,
    Optional,
)
from dataclasses import dataclass, fields
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


_Mouse_Event_Arguments_Fields = [f.name for f in fields(EChartsMouseEventArguments)]
