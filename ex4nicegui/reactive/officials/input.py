from typing import Any, Callable, List, Optional, Dict, Union, cast


from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    to_value,
)

from nicegui import ui
from nicegui.events import handle_event
from .base import BindableUi, DisableableMixin
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class InputBindableUi(
    BindableUi[ui.input],
    DisableableMixin,
    ValueElementMixin[str],
):
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
        validation: Optional[
            Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]
        ] = None,
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

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self
        if prop == "password":
            return self.bind_password(value)

        if prop == "autocomplete":
            return self.bind_autocomplete(value)

        return super().bind_prop(prop, value)

    def bind_autocomplete(self, autocomplete: TGetterOrReadonlyRef[List[str]]):
        """Binds the autocomplete attribute of the input element.

        Args:
            autocomplete (TGetterOrReadonlyRef[List[str]]):  The getter or readonly reference to the autocomplete list.
        """

        @self._ui_signal_on(autocomplete)
        def _():
            self.element.set_autocomplete(to_value(autocomplete))

        return self

    def bind_password(self, password: TGetterOrReadonlyRef[bool]):
        """Binds the password attribute of the input element.

        Args:
            password (TGetterOrReadonlyRef[bool]): The getter or readonly reference to the password state.

        """

        @self._ui_signal_on(password)
        def _():
            self.element._props["type"] = "password" if to_value(password) else "text"
            self.element.update()

        return self

    @property
    def value(self):
        return self.element.value


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
        validation: Optional[Dict[str, Callable[..., bool]]] = None,
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

            @self._ui_effect
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
