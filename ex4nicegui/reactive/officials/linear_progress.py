from typing import (
    Optional,
)
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from nicegui import ui

from .base import BindableUi, _bind_color
from .utils import _convert_kws_ref2value


class LinearProgressBindableUi(BindableUi[ui.linear_progress]):
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

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        return _bind_color(self, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.set_value(to_value(ref_ui))
            self.element.update()

        return self
