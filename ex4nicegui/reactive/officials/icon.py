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

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "name":
            return self.bind_name(value)

        if prop == "color":
            return self.bind_color(value)

        return super().bind_prop(prop, value)

    def bind_name(self, name: TGetterOrReadonlyRef):
        @self._ui_signal_on(name)
        def _():
            self.element.set_name(to_value(name))

        return self
