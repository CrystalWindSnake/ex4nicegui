from typing import (
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier

from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import BindableUi, DisableableMixin
from ex4nicegui.reactive.mixins.backgroundColor import BackgroundColorableMixin
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class CircularProgressBindableUi(
    BindableUi[ui.circular_progress],
    DisableableMixin,
    BackgroundColorableMixin,
    ValueElementMixin[float],
):
    def __init__(
        self,
        value: TMaybeRef[float] = 0.0,
        *,
        min: TMaybeRef[float] = 0.0,  # pylint: disable=redefined-builtin
        max: TMaybeRef[float] = 1.0,  # pylint: disable=redefined-builtin
        size: Optional[TMaybeRef[str]] = "xl",
        show_value: TMaybeRef[bool] = True,
        color: Optional[TMaybeRef[str]] = "primary",
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "value",
                "min",
                "max",
                "color",
                "size",
                "show_value",
            ],
        )

        value_kws = pc.get_values_kws()
        element = ui.circular_progress(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self
        if prop == "color":
            return self.bind_color(value)

        return super().bind_prop(prop, value)
