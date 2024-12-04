from typing import Optional


from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)

from nicegui import ui
from ex4nicegui.reactive.base import BindableUi
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier

from nicegui.elements.spinner import SpinnerTypes


class SpinnerBindableUi(BindableUi[ui.spinner], TextColorableMixin):
    def __init__(
        self,
        type: Optional[SpinnerTypes] = "default",
        *,
        size: TMaybeRef[str] = "1em",
        color: Optional[TMaybeRef[str]] = "primary",
        thickness: TMaybeRef[float] = 5.0,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["type", "size", "color", "thickness"]
        )

        value_kws = pc.get_values_kws()
        element = ui.spinner(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "type":
            raise ValueError("type cannot be bound")
        elif prop == "color":
            return self.bind_color(value)

        return super().bind_prop(prop, value)
