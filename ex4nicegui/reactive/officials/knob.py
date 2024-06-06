from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    to_value,
    TGetterOrReadonlyRef,
)
from nicegui import ui
from .base import BindableUi, DisableableMixin


class KnobBindableUi(
    BindableUi[ui.knob],
    DisableableMixin,
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

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: TGetterOrReadonlyRef[float]):
        @self._ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))

        return self
