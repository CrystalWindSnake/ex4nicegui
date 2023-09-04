from nicegui import ui


from typing_extensions import Literal
from typing import Optional, Union

TBreakpoint = Literal["xs[>0]", "sm[>600]", "md[>1024]", "lg[>1440]", "xl[>1920]"]


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
