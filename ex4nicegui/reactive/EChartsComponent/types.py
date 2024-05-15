from typing import (
    Any,
    Callable,
)
from typing_extensions import Literal
from .event import EChartsMouseEventArguments

_Chart_Click_Args = [
    "componentType",
    "seriesType",
    "seriesIndex",
    "seriesName",
    "name",
    "dataIndex",
    "data",
    "dataType",
    "value",
    "color",
]


_T_echats_on_callback = Callable[[EChartsMouseEventArguments], Any]
_T_mouse_event_name = Literal[
    "click",
    "dblclick",
    "mousedown",
    "mousemove",
    "mouseup",
    "mouseover",
    "mouseout",
    "globalout",
    "contextmenu",
]
