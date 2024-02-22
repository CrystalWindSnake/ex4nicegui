from typing import Any, Callable, List, Optional, Dict, cast


from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    effect,
    is_setter_ref,
    to_value,
)

from nicegui import ui
from nicegui.events import handle_event
from .base import BindableUi, DisableableMixin
from ex4nicegui.reactive.utils import ParameterClassifier


class InputBindableUi(BindableUi[ui.input], DisableableMixin):
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
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.input(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

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
        org_value = value
        is_setter_value = is_setter_ref(value)
        if is_setter_value:
            value = to_value(value)

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

        if is_setter_value:
            ref = cast(Ref, org_value)

            ele = self.element

            @effect
            def _():
                ele.value = ref.value

            def onValueChanged(e):
                has_change = ref.value != ele.value
                ref.value = ele.value or ""

                if has_change:
                    handle_event(on_change, e)

            def on_clear(e):
                ref.value = ""

            ele.on("blur", onValueChanged)
            ele.on("keyup.enter", onValueChanged)
            ele.on("clear", on_clear)
