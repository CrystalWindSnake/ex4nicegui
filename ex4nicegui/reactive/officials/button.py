from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.apiEffect import ui_effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import BindableUi, _bind_color, DisableableMixin


class ButtonBindableUi(BindableUi[ui.button], DisableableMixin):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        on_click: Optional[Callable[..., Any]] = None,
        color: Optional[TMaybeRef[str]] = "primary",
        icon: Optional[TMaybeRef[str]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["text", "color", "icon"], events=["on_click"]
        )

        element = ui.button(**pc.get_values_kws())

        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)
        if prop == "icon":
            return self.bind_icon(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @ui_effect
        def _():
            ele = self.element
            ele._props["label"] = to_value(ref_ui)
            ele.update()

        return self

    def bind_icon(self, ref_ui: ReadonlyRef):
        @ui_effect
        def _():
            ele = self.element
            ele._props["icon"] = to_value(ref_ui)
            ele.update()

        return self
