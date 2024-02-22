from typing import Any, Optional, Callable
from nicegui import ui
from nicegui.events import handle_event
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from .base import SingleValueBindableUi


class ExpansionBindableUi(SingleValueBindableUi[bool, ui.expansion]):
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
            events=["on_value_change"],
        )

        value_kws = pc.get_values_kws()

        value_ref = to_ref(value)

        def inject_on_change(e):
            value_ref.value = e.value
            if on_value_change:
                handle_event(on_value_change, e)

        value_kws.update({"on_value_change": inject_on_change})

        element = ui.expansion(**value_kws)
        super().__init__(value_ref, element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: TMaybeRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: TMaybeRef):
        @effect
        def _():
            self.element.set_value(to_value(ref_ui))
            self.element.update()

        return self

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
