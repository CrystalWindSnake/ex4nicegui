from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Dict,
)
from signe import effect
from ex4nicegui.utils.signals import (
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class NumberBindableUi(SingleValueBindableUi[float, ui.number]):
    @staticmethod
    def _setup_(binder: "NumberBindableUi"):
        def onValueChanged(e):
            binder._ref.value = e.args  # type: ignore

        @effect
        def _():
            binder.element.value = binder.value

        binder.element.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: Optional[TMaybeRef[float]] = None,
        min: Optional[TMaybeRef[float]] = None,
        max: Optional[TMaybeRef[float]] = None,
        step: Optional[TMaybeRef[float]] = None,
        prefix: Optional[TMaybeRef[str]] = None,
        suffix: Optional[TMaybeRef[str]] = None,
        format: Optional[TMaybeRef[str]] = None,
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value,
            "min": min,
            "max": max,
            "step": step,
            "prefix": prefix,
            "suffix": suffix,
            "format": format,
            "on_change": on_change,
            "validation": validation,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.number(**value_kws)
        element.classes("min-w-[10rem]")

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)

        NumberBindableUi._setup_(self)
