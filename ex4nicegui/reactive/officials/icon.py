from typing import (
    Optional,
    cast,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
)
from .base import BindableUi
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin


class IconBindableUi(BindableUi[ui.icon], TextColorableMixin):
    def __init__(
        self,
        name: TMaybeRef[str],
        *,
        size: Optional[TMaybeRef[str]] = None,
        color: Optional[TMaybeRef[str]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["name", "size", "color"], events=[]
        )

        element = ui.icon(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "name":
            return self.bind_name(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_name(self, ref_ui: TGetterOrReadonlyRef):
        @self._ui_effect
        def _():
            ele = cast(TextColorElement, self.element)
            ele._props["name"] = to_value(ref_ui)
            ele.update()

        return self
