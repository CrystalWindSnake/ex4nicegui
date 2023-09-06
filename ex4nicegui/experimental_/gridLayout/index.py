from nicegui import ui


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


class GridFlex(ui.element):
    def __init__(self) -> None:
        """ """
        super().__init__("div")
        self._classes = ["grid"]

    @staticmethod
    def set_classes(
        grid_flex: "GridFlex",
        type: _TGrid_Type,
        template: str,
        horizontal: THorizontal = "stretch",
        vertical: TVertical = "stretch",
        gap: Union[str, float, int] = 1,
        width_full=True,
        break_point: Optional[TBreakpoint] = None,
    ):
        _template = template.strip().replace(" ", "_")
        _type = f"{type}s"
        _justify_items = f"justify-items-{Horizontal_map[horizontal]}"
        _align_items = f"items-{Vertical_map[vertical]}"
        _gap = f"gap-[{_gap_value(gap)}]"
        _w_full = "w-full" if width_full else ""

        class_names = [
            f"grid-{_type}-[{_template}]",
            _justify_items,
            _align_items,
            _gap,
            _w_full,
        ]

        if break_point is not None:
            class_names = [f"{Breakpoint_map[break_point]}-{n}" for n in class_names]

        grid_flex.classes(" ".join(class_names))
        return grid_flex

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
        return GridFlex.set_classes(
            self, type, template, horizontal, vertical, gap, width_full, break_point
        )


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

    return GridFlex.set_classes(
        gf, type, template, horizontal, vertical, gap, width_full, break_point
    )


def column(
    template: str,
    horizontal: THorizontal = "stretch",
    vertical: TVertical = "stretch",
    gap: Union[str, float, int] = 1,
    width_full=True,
):
    gap = f"gap-[{_gap_value(gap)}]"
    w_full = "w-full" if width_full else ""

    box = ui.element("div").classes(f"grid {gap} {w_full}")
    box._style["grid-template-rows"] = template
    box._style["justify-items"] = Horizontal_map[horizontal]
    box._style["align-items"] = Vertical_map[vertical]
    return box


def row(
    template: str,
    vertical: TVertical = "stretch",
    horizontal: THorizontal = "stretch",
    gap: Union[str, float, int] = 1,
    width_full=True,
):
    gap = f"gap-[{_gap_value(gap)}]"
    w_full = "w-full" if width_full else ""

    box = ui.element("div").classes(f"grid {gap} {w_full}")
    box._style["grid-template-columns"] = template
    box._style["justify-items"] = Horizontal_map[horizontal]
    box._style["align-items"] = Vertical_map[vertical]
    return box


def item(
    *, horizontal: Optional[THorizontal] = None, vertical: Optional[TVertical] = None
):
    res = []
    if horizontal is not None:
        res.append(f"justify-self-{Horizontal_map[horizontal]}")

    if vertical is not None:
        res.append(f"self-{Vertical_map[vertical]}")
    return " ".join(res)
