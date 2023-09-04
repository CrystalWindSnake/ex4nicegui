from typing import Any, Callable, Optional, cast
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui import ui, app
from nicegui.element import Element
from signe import createSignal, effect, batch
from ex4nicegui.utils.signals import ref_from_signal

from typing_extensions import Literal
from typing import Optional, Union


TBreakpoint = Literal[
    "xs[0px]",
    "sm[600px]",
    "md[1024px]",
    "lg[1440px]",
    "xl[1920px]",
    ">xs[0px]",
    "<sm[600px]",
    ">sm[600px]",
    "<md[1024px]",
    ">md[1024px]",
    "<lg[1440px]",
    ">lg[1440px]",
    "<xl[1920px]",
    ">xl[1920px]",
]

Breakpoint_map = {
    "xs[0px]": "xs",
    "sm[600px]": "sm",
    "md[1024px]": "md",
    "lg[1440px]": "lg",
    "xl[1920px]": "xl",
    ">xs[0px]": "gt-xs",
    "<sm[600px]": "lt-sm",
    ">sm[600px]": "gt-sm",
    "<md[1024px]": "lt-md",
    ">md[1024px]": "gt-md",
    "<lg[1440px]": "lt-lg",
    ">lg[1440px]": "gt-lg",
    "<xl[1920px]": "lt-xl",
    ">xl[1920px]": "gt-xl",
}


def _gap_value(value: Union[str, float, int]):
    if isinstance(value, (float, int)):
        value = f"{value}rem"
    return value


THorizontal = Literal["left", "center", "right", "stretch"]
Horizontal_map = {
    "left": "start",
    "center": "center",
    "right": "end",
    "stretch": "stretch",
}

TVertical = Literal["top", "center", "bottom", "stretch"]
Vertical_map = {
    "top": "start",
    "center": "center",
    "bottom": "end",
    "stretch": "stretch",
}

_TGrid_Type = Literal["row", "column"]
Grid_Type_map = {
    "row": "columns",
    "column": "rows",
}


class GridFlex(Element, component="GridFlex.js"):
    def __init__(self) -> None:
        super().__init__()

        self._props["normalStyles"] = {}
        self._props["breakpointStyleMap"] = {}

        self.__breakpointStyleMap = {}

    @staticmethod
    def to_styles(
        type: _TGrid_Type,
        template: str,
        horizontal: THorizontal = "stretch",
        vertical: TVertical = "stretch",
        gap: Union[str, float, int] = 1,
        width_full=True,
    ):
        styles = {
            f"grid-template-{Grid_Type_map[type]}": template,
            "justify-items": Horizontal_map[horizontal],
            "align-items": Vertical_map[vertical],
            "gap": _gap_value(gap),
        }

        if width_full:
            styles.update({"width": "100%"})

        return styles

    def grid_flex(
        self,
        type: _TGrid_Type,
        template: str,
        *,
        horizontal: THorizontal = "stretch",
        vertical: TVertical = "stretch",
        gap: Union[str, float, int] = 1,
        width_full=True,
        break_point: Optional[TBreakpoint] = None,
    ):
        styles = GridFlex.to_styles(
            type, template, horizontal, vertical, gap, width_full
        )

        if break_point is None:
            self._props["normalStyles"] = styles
        else:
            self.__breakpointStyleMap[Breakpoint_map[break_point]] = styles
            self._props["breakpointStyleMap"] = self.__breakpointStyleMap

        self.update()
        return self


def grid_flex(
    type: _TGrid_Type,
    template: str,
    *,
    horizontal: THorizontal = "stretch",
    vertical: TVertical = "stretch",
    gap: Union[str, float, int] = 1,
    width_full=True,
    break_point: Optional[TBreakpoint] = None,
):
    # styles = GridFlex.to_styles(type, template, horizontal, vertical, gap, width_full)

    gf = GridFlex()

    gf.grid_flex(
        type,
        template,
        horizontal=horizontal,
        vertical=vertical,
        gap=gap,
        width_full=width_full,
        break_point=break_point,
    )

    return gf
