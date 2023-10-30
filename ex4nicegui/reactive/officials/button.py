from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi, _bind_color, DisableableBindableUi
from .utils import _convert_kws_ref2value


class ButtonBindableUi(
    SingleValueBindableUi[str, ui.button], DisableableBindableUi[ui.button]
):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        on_click: Optional[Callable[..., Any]] = None,
        color: Optional[TMaybeRef[str]] = "primary",
        icon: Optional[TMaybeRef[str]] = None,
    ) -> None:
        kws = {
            "text": text,
            "color": color,
            "icon": icon,
            "on_click": on_click,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.button(**value_kws)

        super().__init__(text, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)
        if prop == "icon":
            return self.bind_icon(ref_ui)
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        return _bind_color(self, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            ele._props["label"] = ref_ui.value
            ele.update()

        return self

    def bind_icon(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            ele._props["icon"] = ref_ui.value
            ele.update()

        return self
