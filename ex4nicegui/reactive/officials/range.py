from typing import Any, Callable, Optional, Dict, cast


from ex4nicegui.utils.signals import to_value, is_setter_ref
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
)

from nicegui import ui
from nicegui.events import handle_event
from ex4nicegui.reactive.base import BindableUi, DisableableMixin
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class RangeBindableUi(
    BindableUi[ui.range],
    DisableableMixin,
    ValueElementMixin[Dict[str, int]],
):
    def __init__(
        self,
        *,
        min: TMaybeRef[float],  # pylint: disable=redefined-builtin
        max: TMaybeRef[float],  # pylint: disable=redefined-builtin
        step: TMaybeRef[float] = 1.0,
        value: Optional[TMaybeRef[Dict[str, int]]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["min", "max", "step", "value"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.range(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return cast(Dict[str, int], self.element.value)


class LazyRangeBindableUi(
    RangeBindableUi,
):
    def __init__(
        self,
        *,
        min: TMaybeRef[float],  # pylint: disable=redefined-builtin
        max: TMaybeRef[float],  # pylint: disable=redefined-builtin
        step: TMaybeRef[float] = 1.0,
        value: Optional[TMaybeRef[Dict[str, int]]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        """A lazy version of `rxui.range` that only updates the value when the user releases the range.

        Args:
            min (TMaybeRef[float]): lower bound of the range
            max (TMaybeRef[float]): upper bound of the range
            step (TMaybeRef[float], optional): step size. Defaults to 1.0.
            value (Optional[TMaybeRef[Dict[str, int]]], optional): initial value to set min and max position of the range. Defaults to None.
            on_change (Optional[Callable[..., Any]], optional): callback which is invoked when the user releases the range. Defaults to None.
        """
        super().__init__(
            min=min,
            max=max,
            step=step,
            value=lambda: to_value(value),  # type: ignore
        )

        if is_setter_ref(value):

            def new_on_change(e):
                value.set_value(e.args)  # type: ignore
                handle_event(on_change, e)

            self.on("change", new_on_change)
