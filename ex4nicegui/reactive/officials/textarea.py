from typing import (
    Any,
    Callable,
    Optional,
    Dict,
)
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class TextareaBindableUi(SingleValueBindableUi[str, ui.textarea]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        value_ref = to_ref(value)
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value_ref,
            "validation": validation,
        }

        value_kws = _convert_kws_ref2value(kws)

        self._setup_on_change(value_ref, value_kws, on_change)

        element = ui.textarea(**value_kws)

        super().__init__(value_ref, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[str]):
        @effect
        def _():
            self.element.set_value(ref_ui.value)
            self.element.update()

        return self

    def _setup_on_change(
        self,
        value_ref: Ref[str],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        def inject_on_change(e):
            value_ref.value = e.value
            if on_change:
                handle_event(on_change, e)

        value_kws.update({"on_change": inject_on_change})


class LazyTextareaBindableUi(TextareaBindableUi):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        super().__init__(
            label,
            placeholder=placeholder,
            value=value,
            on_change=None,
            validation=validation,
        )

        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged(e):
            self._ref.value = ele.value
            if on_change:
                handle_event(on_change, e)

        ele.on("blur", onValueChanged)
        ele.on("keyup.enter", onValueChanged)

    def _setup_on_change(
        self,
        value_ref: Ref[str],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        pass
