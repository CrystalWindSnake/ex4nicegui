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
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class SwitchBindableUi(SingleValueBindableUi[bool, ui.switch]):
    @staticmethod
    def _setup_(binder: "SwitchBindableUi"):
        def onValueChanged(e):
            ele._send_update_on_value_change = ele.LOOPBACK
            cur_value = ele._event_args_to_value(e)
            ele.set_value(cur_value)
            ele._send_update_on_value_change = True
            binder._ref.value = cur_value

        ele = cast(ValueElement, binder.element)

        @effect
        def _():
            ele.value = binder.value

        ele.on("update:modelValue", onValueChanged, [None], throttle=0)  # type: ignore

    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {"text": text, "value": value, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        element = ui.switch(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        SwitchBindableUi._setup_(self)

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
