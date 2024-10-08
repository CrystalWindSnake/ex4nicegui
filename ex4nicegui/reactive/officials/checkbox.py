from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi, DisableableMixin
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


T = TypeVar("T")


class CheckboxBindableUi(
    BindableUi[ui.checkbox], DisableableMixin, ValueElementMixin[bool]
):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["text", "value"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()
        element = ui.checkbox(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)
