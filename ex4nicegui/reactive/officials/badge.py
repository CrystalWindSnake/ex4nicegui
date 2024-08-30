from typing import Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.backgroundColor import BackgroundColorableMixin
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin


class BadgeBindableUi(
    BindableUi[ui.badge],
    BackgroundColorableMixin,
    TextColorableMixin,
):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        color: Optional[TMaybeRef[str]] = "primary",
        text_color: Optional[TMaybeRef[str]] = None,
        outline: TMaybeRef[bool] = False,
    ) -> None:
        """Badge

        A badge element wrapping Quasar's
        `QBadge <https://quasar.dev/vue-components/badge>`_ component.

        :param text: the initial value of the text field
        :param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        :param outline: use 'outline' design (colored text and borders only) (default: False)
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "text",
                "color",
                "text_color",
                "outline",
            ],
            events=[],
        )

        element = ui.badge(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def text(self):
        return self.element.text

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "text":
            return self.bind_text(value)

        if prop == "color":
            return self.bind_color(value)
        if prop == "text-color":
            return self.bind_text_color(value)

        return super().bind_prop(prop, value)

    def bind_color(self, color: TGetterOrReadonlyRef):
        """Binds the background color property of the chip to a ui element.

        Args:
            color (TGetterOrReadonlyRef): background color ui element or getter function

        """
        BackgroundColorableMixin.bind_color(self, color)
        return self

    def bind_text_color(self, color: TGetterOrReadonlyRef):
        """Binds the text color property of the chip to a ui element.

        Args:
            color (TGetterOrReadonlyRef):  text color ui element or getter function


        """
        TextColorableMixin.bind_color(self, color)
        return self

    def bind_text(self, text: TGetterOrReadonlyRef):
        """Binds the text property of the chip to a ui element.

        Args:
            text (TGetterOrReadonlyRef):  text ui element or getter function

        """

        @self._ui_signal_on(text)
        def _():
            self.element.set_text(str(to_value(text)))

        return self
