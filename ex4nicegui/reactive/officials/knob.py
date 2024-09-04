from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    TGetterOrReadonlyRef,
)
from nicegui import ui
from .base import BindableUi, DisableableMixin
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class KnobBindableUi(
    BindableUi[ui.knob], DisableableMixin, TextColorableMixin, ValueElementMixin[float]
):
    def __init__(
        self,
        value: TMaybeRef[float] = 0.0,
        *,
        min: TMaybeRef[float] = 0.0,  # pylint: disable=redefined-builtin
        max: TMaybeRef[float] = 1.0,  # pylint: disable=redefined-builtin
        step: TMaybeRef[float] = 0.01,
        color: Optional[TMaybeRef[str]] = "primary",
        center_color: Optional[TMaybeRef[str]] = None,
        track_color: Optional[TMaybeRef[str]] = None,
        size: Optional[TMaybeRef[str]] = None,
        show_value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "value",
                "min",
                "max",
                "step",
                "color",
                "center_color",
                "track_color",
                "size",
                "show_value",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()
        element = ui.knob(**value_kws)
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
