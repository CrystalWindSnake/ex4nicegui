from __future__ import annotations
from typing import TYPE_CHECKING, Literal, cast
from ex4nicegui.utils.signals import effect, to_value
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
    QUASAR_COLORS,
    TAILWIND_COLORS,
)

if TYPE_CHECKING:
    from ex4nicegui.reactive.officials.base import BindableUi
    from ex4nicegui import TGetterOrReadonlyRef


_color_sys_type = Literal["QUASAR", "TAILWIND", "STYLE"]
_color_attr_name = "data-ex4ng-color"


def bind_color(bindable_ui: BindableUi, ref_ui: TGetterOrReadonlyRef):
    @bindable_ui._ui_effect
    def _():
        ele = cast(TextColorElement, bindable_ui.element)
        color = to_value(ref_ui)

        # get exists color
        # e.g 'QUASAR:red'
        pre_color = ele._props.get(_color_attr_name)  # type: str | None
        if pre_color:
            color_sys, value = pre_color.split(":")  # type: ignore
            color_sys: _color_sys_type

            if color_sys == "QUASAR":
                del ele._props[ele.TEXT_COLOR_PROP]
            elif color_sys == "TAILWIND":
                ele.classes(remove=value)
            else:
                del ele._style["color"]

        cur_sys: _color_sys_type = "STYLE"
        cur_color = color

        if color in QUASAR_COLORS:
            ele._props[ele.TEXT_COLOR_PROP] = color
            cur_sys = "QUASAR"
        elif color in TAILWIND_COLORS:
            cur_color = f"text-{color}"
            ele.classes(replace=cur_color)
            cur_sys = "TAILWIND"
        elif color is not None:
            ele._style["color"] = color

        ele._props[_color_attr_name] = f"{cur_sys}:{color}"

        ele.update()

    return bindable_ui
