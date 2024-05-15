from typing import (
    Union,
)
from typing_extensions import Literal


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

_T_generic_event_name = Literal[
    "highlight",
    "downplay",
    "selectchanged",
    "legendselectchanged",
    "legendselected",
    "legendunselected",
    "legendselectall",
    "legendinverseselect",
    "legendscroll",
    "datazoom",
    "datarangeselected",
    "graphroam",
    "georoam",
    "treeroam",
    "timelinechanged",
    "timelineplaychanged",
    "restore",
    "dataviewchanged",
    "magictypechanged",
    "geoselectchanged",
    "geoselected",
    "geounselected",
    "axisareaselected",
    "brush",
    "brushEnd",
    "brushselected",
    "globalcursortaken",
    "rendered",
    "finished",
]

_T_event_name = Union[_T_mouse_event_name, _T_generic_event_name]
