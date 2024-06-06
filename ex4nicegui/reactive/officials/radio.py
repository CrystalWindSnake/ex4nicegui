from typing import (
    Any,
    Callable,
    List,
    Optional,
    TypeVar,
    cast,
    Dict,
    Union,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.apiEffect import ui_effect

from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from .base import BindableUi

T = TypeVar("T")


class RadioBindableUi(BindableUi[ui.radio]):
    def __init__(
        self,
        options: Union[TMaybeRef[List], TMaybeRef[Dict]],
        *,
        value: TMaybeRef[Any] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "options",
                "value",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.radio(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: TGetterOrReadonlyRef):
        @ui_effect
        def _():
            self.element.set_options(to_value(ref_ui))

        return self

    def bind_value(self, ref_ui: TGetterOrReadonlyRef):
        @ui_effect
        def _():
            cast(ValueElement, self.element).set_value(to_value(ref_ui))

        return self
