from typing import Any, Callable, Dict, Optional, cast
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui import ui, app
from nicegui.element import Element
from signe import createSignal, effect, batch
from ex4nicegui.utils.signals import ref_from_signal

from typing_extensions import Literal
from typing import Optional, Union
from . import utils


TBreakpoint = Literal[
    "xs[0px-599.99px]",
    "sm[600px-1023.99px]",
    "md[1024px-1439.99px]",
    "lg[1440px-1919.99px]",
    "xl[1920px-Infinity]",
    ">xs[600px-Infinity]",
    "<sm[0-599.99px]",
    ">sm[1024px-Infinity]",
    "<md[0-1023.99px]",
    ">md[1440px-Infinity]",
    "<lg[0-1439.99px]",
    ">lg[1920px-Infinity]",
    "<xl[0-1919.99px]",
]

Breakpoint_map = {
    "xs[0px-599.99px]": "xs",
    "sm[600px-1023.99px]": "sm",
    "md[1024px-1439.99px]": "md",
    "lg[1440px-1919.99px]": "lg",
    "xl[1920px-Infinity]": "xl",
    ">xs[600px-Infinity]": "gt-xs",
    "<sm[0-599.99px]": "lt-sm",
    ">sm[1024px-Infinity]": "gt-sm",
    "<md[0-1023.99px]": "lt-md",
    ">md[1440px-Infinity]": "gt-md",
    "<lg[0-1439.99px]": "lt-lg",
    ">lg[1920px-Infinity]": "gt-lg",
    "<xl[0-1919.99px]": "lt-xl",
}


def _gap_value(value: Optional[Union[str, float, int]]):
    if value is None:
        return value

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
    def _cleanStyle(styles: Dict):
        return {k: v for k, v in styles.items() if v is not None}

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

    def grid_box(
        self,
        area: Optional[str] = None,
        *,
        template_rows: Optional[str] = None,
        template_columns: Optional[str] = None,
        horizontal: THorizontal = "stretch",
        vertical: TVertical = "stretch",
        gap: Optional[Union[str, float, int]] = 1,
        width_full=True,
        break_point: Optional[TBreakpoint] = None,
        **kws,
    ):
        if area is not None:
            areas_list = utils.areas_str2array(area)
            area = utils.areas_array2str(areas_list)

        styles = {
            "grid-template-areas": area,
            "grid-template-rows": template_rows,
            "grid-template-columns": template_columns,
            "justify-items": Horizontal_map[horizontal],
            "align-items": Vertical_map[vertical],
            "gap": _gap_value(gap),
        }
        styles.update(kws)

        if width_full:
            styles.update({"width": "100%"})

        styles = GridFlex._cleanStyle(styles)

        if break_point is None:
            self._props["normalStyles"] = styles
        else:
            self.__breakpointStyleMap[Breakpoint_map[break_point]] = styles
            self._props["breakpointStyleMap"] = self.__breakpointStyleMap

        self.update()
        return self


def grid_box(
    area: Optional[str] = None,
    *,
    template_rows: Optional[str] = None,
    template_columns: Optional[str] = None,
    horizontal: THorizontal = "stretch",
    vertical: TVertical = "stretch",
    gap: Union[str, float, int] = 1,
    width_full=True,
    break_point: Optional[TBreakpoint] = None,
    **kws,
):
    gf = GridFlex()

    gf.grid_box(
        area,
        template_rows=template_rows,
        template_columns=template_columns,
        horizontal=horizontal,
        vertical=vertical,
        gap=gap,
        width_full=width_full,
        break_point=break_point,
        **kws,
    )

    return gf


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


class MarkArea:
    def __init__(self, mark: str) -> None:
        self.mark = mark

    def __radd__(self, other: ui.element):
        other.style(f"grid-area:{self.mark}")
        return other


def mark_area(mark: str):
    return MarkArea(mark)


class ItemPosition:
    def __init__(
        self,
        horizontal: Optional[THorizontal] = None,
        vertical: Optional[TVertical] = None,
    ) -> None:
        self.horizontal = horizontal
        self.vertical = vertical

    def __radd__(self, other: ui.element):
        res = []
        if self.horizontal is not None:
            res.append(f"justify-self-{Horizontal_map[self.horizontal]}")

        if self.vertical is not None:
            res.append(f"self-{Vertical_map[self.vertical]}")

        other.classes(" ".join(res))

        return other


def item_position(
    *, horizontal: Optional[THorizontal] = None, vertical: Optional[TVertical] = None
):
    return ItemPosition(horizontal, vertical)
