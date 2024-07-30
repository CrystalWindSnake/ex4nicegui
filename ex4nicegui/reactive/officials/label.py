from typing import Any
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi, TextColorableMixin


class LabelBindableUi(BindableUi[ui.label], TextColorableMixin):
    def __init__(
        self,
        text: TMaybeRef[Any] = "",
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["text"], events=[])

        element = ui.label(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def text(self):
        return self.element.text

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_text(self, ref_ui: TGetterOrReadonlyRef):
        @self._ui_effect
        def _():
            self.element.set_text(str(to_value(ref_ui)))
            self.element.update()

        return self
