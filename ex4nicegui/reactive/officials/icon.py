from typing import (
    Optional,
    cast,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
)
from nicegui import ui
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
)
from .base import SingleValueBindableUi, _bind_color
from .utils import _convert_kws_ref2value


class IconBindableUi(SingleValueBindableUi[str, ui.icon]):
    def __init__(
        self,
        name: TMaybeRef[str],
        *,
        size: Optional[TMaybeRef[str]] = None,
        color: Optional[TMaybeRef[str]] = None,
    ) -> None:
        kws = {
            "name": name,
            "size": size,
            "color": color,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.icon(**value_kws)

        super().__init__(name, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "name":
            return self.bind_name(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        return _bind_color(self, ref_ui)

    def bind_name(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = cast(TextColorElement, self.element)
            ele._props["name"] = ref_ui.value
            ele.update()

        return self
