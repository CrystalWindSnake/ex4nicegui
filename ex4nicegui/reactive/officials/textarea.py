from typing import (
    Any,
    Callable,
    Optional,
    Dict,
    cast,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import BindableUi
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class TextareaBindableUi(BindableUi[ui.textarea], ValueElementMixin[str]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Optional[Dict[str, Callable[..., bool]]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "label",
                "placeholder",
                "value",
                "validation",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.textarea(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)


class LazyTextareaBindableUi(TextareaBindableUi):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
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
            on_change=None,
            validation=validation,
        )

        if is_setter_value:
            ref = cast(Ref, org_value)
            ele = self.element

            @self._ui_effect
            def _():
                ele.value = ref.value

            def onValueChanged(e):
                ref.value = ele.value
                if on_change:
                    handle_event(on_change, e)

            def on_clear(e):
                ref.value = ""

            ele.on("blur", onValueChanged)
            ele.on("keyup.enter", onValueChanged)
            ele.on("clear", on_clear)
