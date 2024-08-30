from typing import Any, Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    to_raw,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.backgroundColor import BackgroundColorableMixin
from ex4nicegui.reactive.mixins.textColor import TextColorableMixin


class AvatarBindableUi(
    BindableUi[ui.avatar], TextColorableMixin, BackgroundColorableMixin
):
    def __init__(
        self,
        icon: Optional[TMaybeRef[str]] = None,
        *,
        color: Optional[TMaybeRef[str]] = "primary",
        text_color: Optional[TMaybeRef[str]] = None,
        size: Optional[TMaybeRef[str]] = None,
        font_size: Optional[TMaybeRef[str]] = None,
        square: TMaybeRef[bool] = False,
        rounded: TMaybeRef[bool] = False,
    ) -> None:
        """Avatar

        A avatar element wrapping Quasar's
        `QAvatar <https://quasar.dev/vue-components/avatar>`_ component.

        :param icon: name of the icon or image path with "img:" prefix (e.g. "map", "img:path/to/image.png")
        :param color: background color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param text_color: color name from the Quasar Color Palette (e.g. "primary", "teal-10")
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl) (e.g. "16px", "2rem")
        :param font_size: size in CSS units, including unit name, of the content (icon, text) (e.g. "18px", "2rem")
        :param square: removes border-radius so borders are squared (default: False)
        :param rounded: applies a small standard border-radius for a squared shape of the component (default: False)
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "icon",
                "color",
                "text_color",
                "size",
                "font_size",
                "square",
                "rounded",
            ],
            events=[],
        )

        init_kws = pc.get_values_kws()
        element = ui.avatar(**init_kws)
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
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
