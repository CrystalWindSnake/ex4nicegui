from typing import (
    Any,
    Callable,
    Optional,
    Dict,
    cast,
)
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.apiEffect import ui_effect
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
from .base import BindableUi


class TextareaBindableUi(BindableUi[ui.textarea]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
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

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[str]):
        @ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))

        return self


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

            @effect
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
