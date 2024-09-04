from typing import (
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui

from .base import BindableUi
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class LinearProgressBindableUi(
    BindableUi[ui.linear_progress], TextColorableMixin, ValueElementMixin[float]
):
    def __init__(
        self,
        value: TMaybeRef[float] = 0.0,
        *,
        size: Optional[TMaybeRef[str]] = None,
        show_value: TMaybeRef[bool] = True,
        color: Optional[TMaybeRef[str]] = "primary",
    ) -> None:
        """Linear Progress

        A linear progress bar wrapping Quasar's
        `QLinearProgress <https://quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (from 0.0 to 1.0)
        :param size: the height of the progress bar (default: "20px" with value label and "4px" without)
        :param show_value: whether to show a value label in the center (default: `True`)
        :param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        """
        pc = ParameterClassifier(
            locals(), maybeRefs=["value", "size", "show_value", "color"], events=[]
        )

        element = ui.linear_progress(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        if prop == "color":
            return self.bind_color(value)

        return super().bind_prop(prop, value)
