from typing import Any, Callable, Optional, Dict


from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
)

from nicegui import ui
from ex4nicegui.reactive.base import BindableUi, DisableableMixin
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class RangeBindableUi(
    BindableUi[ui.range],
    DisableableMixin,
    ValueElementMixin[str],
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
        return self.element.value
