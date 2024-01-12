from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
)
from nicegui import ui
from .base import SingleValueBindableUi, DisableableBindableUi
from .utils import _convert_kws_ref2value


_TSliderValue = TypeVar("_TSliderValue", float, int, None)


class SliderBindableUi(
    SingleValueBindableUi[Optional[_TSliderValue], ui.slider],
    DisableableBindableUi[ui.slider],
):
    def __init__(
        self,
        min: TMaybeRef[_TSliderValue],
        max: TMaybeRef[_TSliderValue],
        step: TMaybeRef[_TSliderValue] = 1.0,
        value: Optional[TMaybeRef[_TSliderValue]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {
            "min": min,
            "max": max,
            "step": step,
            "value": value,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        def inject_on_change(e):
            self._ref.value = e.value
            if on_change:
                on_change(e)

        value_kws.update({"on_change": inject_on_change})

        element = ui.slider(**value_kws).props("label label-always switch-label-side")

        super().__init__(value, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value) and key != "value":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[float]):
        @effect
        def _():
            self.element.set_value(ref_ui.value)
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
        super().__init__(min, max, step, value, on_change)

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged():
            self._ref.value = ele.value

        ele.on("change", onValueChanged)
