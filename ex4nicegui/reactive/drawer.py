from typing_extensions import Literal
from nicegui import ui
from ex4nicegui.reactive.officials import DrawerBindableUi
from signe import effect
from typing import Union, Optional

_TDrawerSide = Literal["left", "right"]


def drawer(
    side: _TDrawerSide = "left",
    overlay=False,
    *,
    value: Optional[bool] = None,
    fixed: bool = False,
    bordered: bool = True,
    elevated: bool = False,
    top_corner: bool = False,
    bottom_corner: bool = False,
):
    kws = {
        "value": value,
        "fixed": fixed,
        "bordered": bordered,
        "elevated": elevated,
        "top_corner": top_corner,
        "bottom_corner": bottom_corner,
    }

    ele = None

    if side == "left":
        ele = ui.left_drawer(**kws)
    else:
        ele = ui.right_drawer(**kws)

    ele.style(f"background-color:rgba(25, 118, 210,0.3)")
    ele.classes("flex flex-col gap-4")

    init_value = (
        ele._props["model-value"]
        if "model-value" in ele._props
        else ele._props["show-if-above"]
    )
    r = DrawerBindableUi(init_value, ele)

    @effect
    def _():
        value = "true" if r.value else "false"
        ele.props(f":model-value={value}")

    def on_update(args):
        r.value = args["args"]

    ele.on("update:modelValue", on_update)

    return r
