from typing import Any, Callable, List, Optional, Dict


from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)

from nicegui import ui
from nicegui.events import handle_event
from .base import SingleValueBindableUi, DisableableMixin
from ex4nicegui.reactive.utils import ParameterClassifier


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
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "label",
                "value",
                "placeholder",
                "password",
                "password_toggle_button",
                "autocomplete",
                "validation",
            ],
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        value_ref = to_ref(value)

        self._setup_on_change(value_ref, value_kws, on_change)

        element = ui.input(**value_kws)
        super().__init__(value_ref, element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def _setup_on_change(
        self,
        value_ref: Ref[str],
        value_kws: dict,
        on_change: Optional[Callable[..., Any]] = None,
    ):
        def inject_on_change(e):
            value_ref.value = e.value
            handle_event(on_change, e)

        value_kws.update({"on_change": inject_on_change})

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)
        if prop == "password":
            return self.bind_password(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[str]):
        @effect
        def _():
            self.element.set_value(to_value(ref_ui))
            self.element.update()

        return self

    def bind_password(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element._props["type"] = "password" if to_value(ref_ui) else "text"
            self.element.update()

        return self


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

        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged(e):
            has_change = self._ref.value != ele.value
            self._ref.value = ele.value or ""

            if has_change:
                handle_event(on_change, e)

        def on_clear(e):
            self._ref.value = ""

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
