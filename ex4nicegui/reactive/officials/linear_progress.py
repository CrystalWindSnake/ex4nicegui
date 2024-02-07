from typing import (
    Optional,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
)
from nicegui import ui

from .base import SingleValueBindableUi, _bind_color
from .utils import _convert_kws_ref2value


class LinearProgressBindableUi(SingleValueBindableUi[float, ui.linear_progress]):
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
        value_ref = to_ref(value)
        kws = {
            "value": value_ref,
            "size": size,
            "show_value": show_value,
            "color": color,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.linear_progress(**value_kws)

        super().__init__(value_ref, element)

        for key, value in kws.items():
            if is_ref(value):
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
            print(ref_ui.value)
            self.element.set_value(ref_ui.value)
            self.element.update()

        return self
