from typing import Any, Callable, Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class TabsBindableUi(BindableUi[ui.tabs], ValueElementMixin[str]):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["value"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        element = ui.tabs(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)
