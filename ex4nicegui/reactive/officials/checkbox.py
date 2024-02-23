from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.apiEffect import ui_effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import BindableUi, DisableableMixin

T = TypeVar("T")


class CheckboxBindableUi(BindableUi[ui.checkbox], DisableableMixin):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["text", "value"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.checkbox(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))
            self.element.update()

        return self
