from typing import Any
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_value_getter,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class LabelBindableUi(SingleValueBindableUi[Any, ui.label]):
    def __init__(
        self,
        text: TMaybeRef[Any] = "",
    ) -> None:
        kws = {
            "text": text,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.label(**value_kws)

        super().__init__(text, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            color = ref_ui.value
            ele._style["color"] = color
            ele.update()

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.set_text(str(ref_ui.value))
            self.element.update()

        return self
