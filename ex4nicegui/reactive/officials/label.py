from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class LabelBindableUi(SingleValueBindableUi[str, ui.label]):
    @staticmethod
    def _setup_(binder: "LabelBindableUi"):
        def onValueChanged(e):
            binder._ref.value = e.args["label"]  # type: ignore

        @effect
        def _():
            binder.element.text = binder.value

        binder.element.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        text: TMaybeRef[str] = "",
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

        LabelBindableUi._setup_(self)

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
