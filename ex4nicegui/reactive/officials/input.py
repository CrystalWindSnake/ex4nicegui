from typing import Any, Callable, List, Optional, Dict


from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    to_ref,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
)

from nicegui import ui
from nicegui.events import handle_event
from .base import SingleValueBindableUi, DisableableMixin
from .utils import _convert_kws_ref2value


class InputBindableUi(SingleValueBindableUi[str, ui.input], DisableableMixin):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        password: TMaybeRef[bool] = False,
        password_toggle_button: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
        autocomplete: Optional[TMaybeRef[List[str]]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value,
            "password": password,
            "password_toggle_button": password_toggle_button,
            "autocomplete": autocomplete,
            "validation": validation,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        value_ref = to_ref(value)

        self._setup_on_change(value_ref, value_kws, on_change)

        element = ui.input(**value_kws)

        super().__init__(value_ref, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

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


def _nothing():
    pass


class LazyInputBindableUi(InputBindableUi):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        password: TMaybeRef[bool] = False,
        password_toggle_button: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
        autocomplete: Optional[TMaybeRef[List[str]]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        super().__init__(
            label,
            placeholder=placeholder,
            value=value,
            password=password,
            password_toggle_button=password_toggle_button,
            on_change=None,
            autocomplete=autocomplete,
            validation=validation,
        )

        on_change = on_change or _nothing

        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged():
            self._ref.value = ele.value or ""
            on_change()

        def on_clear(_):
            self._ref.value = ""
            on_change()

        ele.on("blur", onValueChanged)
        ele.on("keyup.enter", onValueChanged)
        ele.on("clear", on_clear)

    def _setup_on_change(
        self,
        value_ref: Ref[str],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        pass
