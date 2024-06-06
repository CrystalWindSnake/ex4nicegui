from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    cast,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import BindableUi, DisableableMixin


_TSliderValue = TypeVar("_TSliderValue", float, int, None)


class SliderBindableUi(
    BindableUi[ui.slider],
    DisableableMixin,
):
    def __init__(
        self,
        min: TMaybeRef[_TSliderValue],
        max: TMaybeRef[_TSliderValue],
        step: TMaybeRef[_TSliderValue] = 1.0,
        value: TMaybeRef[_TSliderValue] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "value",
                "min",
                "max",
                "step",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()
        value_kws.update({"value": 0 if value is None else value_kws.get("value")})

        element = ui.slider(**value_kws).props("label label-always switch-label-side")
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
            self.element.update()

        return self


class LazySliderBindableUi(SliderBindableUi):
    def __init__(
        self,
        min: TMaybeRef[_TSliderValue],
        max: TMaybeRef[_TSliderValue],
        step: TMaybeRef[_TSliderValue] = 1,
        value: Optional[TMaybeRef[_TSliderValue]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        org_value = value
        is_setter_value = is_setter_ref(value)
        if is_setter_value:
            value = to_value(value)

        super().__init__(min, max, step, value, on_change)

        if is_setter_value:
            ref = cast(Ref, org_value)
            ele = self.element

            @self._ui_effect
            def _():
                ele.value = ref.value

            def onValueChanged(e):
                ref.value = ele.value
                if on_change:
                    handle_event(on_change, e)

            ele.on("change", onValueChanged)
