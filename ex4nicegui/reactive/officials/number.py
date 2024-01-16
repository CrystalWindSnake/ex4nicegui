from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Dict,
    Union,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    effect,
    is_ref,
    _TMaybeRef as TMaybeRef,
    to_ref,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class NumberBindableUi(SingleValueBindableUi[float, ui.number]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[Union[float, None]] = None,
        min: Optional[TMaybeRef[float]] = None,
        max: Optional[TMaybeRef[float]] = None,
        step: Optional[TMaybeRef[float]] = None,
        prefix: Optional[TMaybeRef[str]] = None,
        suffix: Optional[TMaybeRef[str]] = None,
        format: Optional[TMaybeRef[str]] = None,
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        value_ref = to_ref(value)
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value_ref,
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

        def inject_on_change(e):
            value_ref.value = e.value
            if on_change:
                on_change(e)

        value_kws.update({"on_change": inject_on_change})

        element = ui.number(**value_kws)
        element.classes("min-w-[10rem]")

        super().__init__(value_ref, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[float]):
        @effect
        def _():
            self.element.set_value(ref_ui.value)
            self.element.update()

        return self
