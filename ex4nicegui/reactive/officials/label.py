from typing import Any
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    to_raw,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.textColor import HtmlTextColorableMixin


class LabelBindableUi(BindableUi[ui.label], HtmlTextColorableMixin):
    def __init__(
        self,
        text: TMaybeRef[Any] = "",
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["text"], events=[])

        init_kws = pc.get_values_kws()
        init_kws.update({"text": str(init_kws.get("text", ""))})
        element = ui.label(**init_kws)
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def text(self):
        return self.element.text

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "text":
            return self.bind_text(value)

        if prop == "color":
            return self.bind_color(value)

        return super().bind_prop(prop, value)

    def bind_text(self, text: TGetterOrReadonlyRef):
        @self._ui_signal_on(text, deep=True)
        def _():
            self.element.set_text(str(to_raw(to_value(text))))

        return self
