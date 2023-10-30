from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    cast,
)
from ex4nicegui import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from .base import SingleValueBindableUi, DisableableBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class CheckboxBindableUi(
    SingleValueBindableUi[bool, ui.checkbox], DisableableBindableUi[ui.checkbox]
):
    @staticmethod
    def _setup_(binder: "CheckboxBindableUi"):
        ele = cast(ValueElement, binder.element)

        def onValueChanged(e):
            binder._ref.value = e.args[0]  # type: ignore

        @effect
        def _():
            ele.value = binder.value

        ele.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {"text": text, "value": value, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        element = ui.checkbox(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        CheckboxBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.set_value(ref_ui.value)
            self.element.update()

        return self
