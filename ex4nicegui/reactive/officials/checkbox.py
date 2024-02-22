from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    cast,
)
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from nicegui.elements.mixins.value_element import ValueElement
from .base import SingleValueBindableUi, DisableableMixin

T = TypeVar("T")


class CheckboxBindableUi(SingleValueBindableUi[bool, ui.checkbox], DisableableMixin):
    @staticmethod
    def _setup_(binder: "CheckboxBindableUi"):
        ele = cast(ValueElement, binder.element)

        @effect
        def _():
            ele.value = binder.value

    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["text", "value"], events=["on_change"]
        )

        value_kws = pc.get_values_kws()

        value_ref = to_ref(value)

        def inject_on_change(e):
            value_ref.value = e.value
            handle_event(on_change, e)

        value_kws.update({"on_change": inject_on_change})

        element = ui.checkbox(**value_kws)
        super().__init__(value_ref, element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.set_value(to_value(ref_ui))
            self.element.update()

        return self
