from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Union,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import SingleValueBindableUi, DisableableMixin
from .utils import _convert_kws_ref2value


_TSliderValue = TypeVar("_TSliderValue", float, int, None)


class SliderBindableUi(
    SingleValueBindableUi[Optional[_TSliderValue], ui.slider],
    DisableableMixin,
):
    def __init__(
        self,
        min: TMaybeRef[_TSliderValue],
        max: TMaybeRef[_TSliderValue],
        step: TMaybeRef[_TSliderValue] = 1.0,
        value: TMaybeRef[Union[_TSliderValue, None]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        value_ref = to_ref(0 if value is None else value)  # type: ignore
        kws = {
            "min": min,
            "max": max,
            "step": step,
            "value": value_ref,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        self._setup_on_change(value_ref, value_kws, on_change)  # type: ignore

        element = ui.slider(**value_kws).props("label label-always switch-label-side")

        super().__init__(value_ref, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

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

    def _setup_on_change(
        self,
        value_ref: Ref[_TSliderValue],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        def inject_on_change(e):
            value_ref.value = e.value
            if on_change:
                handle_event(on_change, e)

        value_kws.update({"on_change": inject_on_change})


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

        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged(e):
            self._ref.value = ele.value
            if on_change:
                handle_event(on_change, e)

        ele.on("change", onValueChanged)

    def _setup_on_change(
        self,
        value_ref: Ref[float],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        pass
