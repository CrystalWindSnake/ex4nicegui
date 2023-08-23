from typing import Any, Optional, Callable
from nicegui import ui
from .base import BindableUi
from ex4nicegui.utils.signals import (
    effect,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from .utils import _convert_kws_ref2value
from .base import SingleValueBindableUi


class ExpansionBindableUi(SingleValueBindableUi[bool, ui.expansion]):
    def __init__(
        self,
        text: Optional[TMaybeRef[str]] = None,
        *,
        icon: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[bool] = False,
        on_value_change: Optional[Callable[..., None]] = None
    ) -> None:
        kws = {
            "text": text,
            "icon": icon,
            "value": value,
            "on_value_change": on_value_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.expansion(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value) and key != "value":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onModelValueChanged(e):
            self._ref.value = e.args

        ele.on("update:modelValue", handler=onModelValueChanged)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
