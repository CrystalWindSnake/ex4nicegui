from typing import Any, Callable, Dict, List, Optional, cast, overload
import ex4nicegui.utils.types as types_utils
from nicegui import ui
from .ref import (
    AggridBindableUi,
)


# def color_picker(
#     init_color="rgba(88, 152, 212,1)",
# ) -> SingleValueBindableUi[str, ui.color_picker]:
#     def on_pick(e):
#         r.value = e.color

#     with ui.card().tight():
#         element = ui.color_picker(on_pick=on_pick)
#         element.default_slot.children[0].props(f'format-model="rgba"')

#         ui.button(on_click=element.open, icon="colorize")

#     r = SingleValueBindableUi(init_color, element)

#     return r


@types_utils.mirror_func(ui.aggrid)
def aggrid(options: Dict, *arg, **kws) -> AggridBindableUi:
    if "pagination" not in options:
        options["pagination"] = True

        if "paginationPageSize" not in options:
            options["paginationPageSize"] = 20

    element = ui.aggrid(options, *arg, **kws)
    r = AggridBindableUi(options, element)
    return r
