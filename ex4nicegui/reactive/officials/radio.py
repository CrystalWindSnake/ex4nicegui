from typing import (
    Any,
    Callable,
    List,
    Optional,
    TypeVar,
    cast,
    Dict,
    Union,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
)
from nicegui import ui
from nicegui.events import handle_event
from nicegui.elements.mixins.value_element import ValueElement
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class RadioBindableUi(SingleValueBindableUi[bool, ui.radio]):
    def __init__(
        self,
        options: Union[TMaybeRef[List], TMaybeRef[Dict]],
        *,
        value: TMaybeRef[Any] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        value_ref = to_ref(value)
        kws = {"options": options, "value": value_ref, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        def inject_on_change(e):
            value_ref.value = e.value
            if on_change:
                handle_event(on_change, e)

        value_kws.update({"value": None, "on_change": inject_on_change})

        element = ui.radio(**value_kws)

        super().__init__(value_ref, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.options = ref_ui.value
            self.element.update()

        return self

    def bind_value(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(ValueElement, self.element).set_value(ref_ui.value)

        return self
