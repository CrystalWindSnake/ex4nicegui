from typing import Any, Callable, Dict, Optional, cast, overload
import ex4nicegui.utils.types as types_utils
from nicegui import ui
from .ref import (
    BindableUi,
    TextElementBindableUi,
    ValueElementBindableUi,
    TextColorElementBindableUi,
    AggridBindableUi,
)
from signe import effect


@types_utils.mirror_func(ui.label)
def label(*arg, **kws) -> TextElementBindableUi[ui.label]:
    element = ui.label(*arg, **kws)
    r = TextElementBindableUi(element.text, element)
    return r


@types_utils.mirror_func(ui.input)
def lazy_input(*arg, **kws) -> ValueElementBindableUi[str, ui.input]:
    return _input(lazy=True, *arg, **kws)


@types_utils.mirror_func(ui.input)
def input(*arg, **kws) -> ValueElementBindableUi[str, ui.input]:
    return _input(*arg, **kws)


def _input(*arg, **kws) -> ValueElementBindableUi[str, ui.input]:
    has_lazy = "lazy" in kws
    is_lazy = has_lazy and kws["lazy"]
    if has_lazy:
        del kws["lazy"]
    element = ui.input(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)

    @effect
    def _():
        element.value = r.value

    if is_lazy:

        def onValueChanged():
            r.value = element.value

        element.on("blur", onValueChanged)
        element.on("keyup.enter", onValueChanged)
    else:

        def onValueInput(args):
            r.value = args["args"]

        element.on("update:modelValue", handler=onValueInput)

    return r


@types_utils.mirror_func(ui.textarea)
def lazy_textarea(*arg, **kws) -> ValueElementBindableUi[str, ui.textarea]:
    return _textarea(lazy=True, *arg, **kws)


@types_utils.mirror_func(ui.textarea)
def textarea(*arg, **kws) -> ValueElementBindableUi[str, ui.textarea]:
    return _textarea(*arg, **kws)


def _textarea(*arg, **kws) -> ValueElementBindableUi[str, ui.textarea]:
    has_lazy = "lazy" in kws
    is_lazy = has_lazy and kws["lazy"]
    if has_lazy:
        del kws["lazy"]
    element = ui.textarea(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)

    @effect
    def _():
        element.value = r.value

    if is_lazy:

        def onValueChanged():
            r.value = element.value

        element.on("blur", onValueChanged)
        element.on("keyup.enter", onValueChanged)
    else:

        def onValueInput(args):
            element.value = args["args"]

        element.on("update:modelValue", handler=onValueInput)

    return r


@types_utils.mirror_func(ui.checkbox)
def checkbox(*arg, **kws) -> ValueElementBindableUi[bool, ui.checkbox]:
    element = ui.checkbox(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)
    ValueElementBindableUi._setup_normal(r)
    return r


@types_utils.mirror_func(ui.radio)
def radio(*arg, **kws) -> ValueElementBindableUi[bool, ui.radio]:
    element = ui.radio(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)
    ValueElementBindableUi._setup_radio(r)
    return r


@types_utils.mirror_func(ui.switch)
def switch(*arg, **kws) -> ValueElementBindableUi[bool, ui.switch]:
    element = ui.switch(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)
    ValueElementBindableUi._setup_normal(r)
    return r


@types_utils.mirror_func(ui.select)
def select(*arg, **kws) -> ValueElementBindableUi[str, ui.select]:
    element = ui.select(*arg, **kws)

    r = ValueElementBindableUi(element.value, element)
    ValueElementBindableUi._setup_select(r)
    return r


@types_utils.mirror_func(ui.icon)
def icon(*arg, **kws) -> TextColorElementBindableUi[str, ui.icon]:
    element = ui.icon(*arg, **kws)
    r = TextColorElementBindableUi(element._props["name"], element)
    return r


@types_utils.mirror_func(ui.button)
def button(*arg, **kws) -> BindableUi[str, ui.button]:
    element = ui.button(*arg, **kws)

    r = BindableUi("", element)

    return r


def color_picker(init_color="rgba(88, 152, 212,1)") -> BindableUi[str, ui.color_picker]:
    def on_pick(e):
        r.value = e.color

    with ui.card().tight():
        element = ui.color_picker(on_pick=on_pick)
        element.default_slot.children[0].props(f'format-model="rgba"')

        ui.button(on_click=element.open, icon="colorize")

    r = BindableUi(init_color, element)

    return r


@types_utils.mirror_func(ui.aggrid)
def aggrid(options: Dict, *arg, **kws) -> AggridBindableUi:
    if "pagination" not in options:
        options["pagination"] = True

        if "paginationPageSize" not in options:
            options["paginationPageSize"] = 20

    element = ui.aggrid(options, *arg, **kws)
    r = AggridBindableUi(options, element)
    return r
