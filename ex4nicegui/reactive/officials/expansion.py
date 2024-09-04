from typing import Any, Optional, Callable
from nicegui import ui
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)
from .base import BindableUi


class ExpansionBindableUi(BindableUi[ui.expansion], ValueElementMixin[bool]):
    def __init__(
        self,
        text: Optional[TMaybeRef[str]] = None,
        *,
        caption: Optional[TMaybeRef[str]] = None,
        icon: Optional[TMaybeRef[str]] = None,
        group: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[bool] = False,
        on_value_change: Optional[Callable[..., None]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "text",
                "caption",
                "icon",
                "group",
                "value",
            ],
            v_model=("value", "on_value_change"),
            events=["on_value_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.expansion(**value_kws)
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

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
