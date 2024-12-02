from typing import (
    Any,
    Dict,
    Optional,
)
from dataclasses import dataclass, fields
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import (
    UiEventArguments,
)


@dataclass(**KWONLY_SLOTS)
class EChartsMouseEventArguments(UiEventArguments):
    componentType: Optional[str] = None
    seriesType: Optional[str] = None
    seriesIndex: Optional[int] = None
    seriesName: Optional[str] = None
    name: Optional[str] = None
    dataIndex: Optional[int] = None
    data: Optional[Dict] = None
    dataType: Optional[str] = None
    value: Optional[Any] = None
    color: Optional[str] = None


_Mouse_Event_Arguments_Fields = [f.name for f in fields(EChartsMouseEventArguments)]
