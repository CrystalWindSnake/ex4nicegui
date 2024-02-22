from typing import Any
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.signals import (
    to_value,
    _TMaybeRef as TMaybeRef,
    effect,
)
from nicegui import ui
from .base import BindableUi


class LabelBindableUi(BindableUi[ui.label]):
    def __init__(
        self,
        text: TMaybeRef[Any] = "",
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["text"], events=[])

        element = ui.label(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: TMaybeRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: TMaybeRef):
        @effect
        def _():
            ele = self.element
            color = to_value(ref_ui)
            ele._style["color"] = color
            ele.update()

    def bind_text(self, ref_ui: TMaybeRef):
        @effect
        def _():
            self.element.set_text(str(to_value(ref_ui)))
            self.element.update()

        return self
