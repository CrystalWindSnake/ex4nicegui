from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import (
    BindableUi,
    DisableableMixin,
    BackgroundColorableMixin,
    TextColorableMixin,
)


class ButtonBindableUi(
    BindableUi[ui.button],
    DisableableMixin,
    BackgroundColorableMixin,
    TextColorableMixin,
):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        on_click: Optional[Callable[..., Any]] = None,
        color: Optional[TMaybeRef[str]] = "primary",
        icon: Optional[TMaybeRef[str]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["text", "color", "icon"], events=["on_click"]
        )

        element = ui.button(**pc.get_values_kws())

        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)
        if prop == "icon":
            return self.bind_icon(ref_ui)
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: TGetterOrReadonlyRef[str]):
        """Binds the background color of the button.

        Args:
            ref_ui (TGetterOrReadonlyRef[str]): Getter or readonly reference to the color.

        """
        BackgroundColorableMixin.bind_color(self, ref_ui)
        return self

    def bind_text_color(self, ref_ui: TGetterOrReadonlyRef[str]):
        """Binds the text color of the button.

        Args:
            ref_ui (TGetterOrReadonlyRef[str]):  Getter or readonly reference to the color.

        """
        TextColorableMixin.bind_color(self, ref_ui)
        return self

    def bind_text(self, ref_ui: TGetterOrReadonlyRef):
        @self._ui_effect
        def _():
            ele = self.element
            ele._props["label"] = to_value(ref_ui)
            ele.update()

        return self

    def bind_icon(self, ref_ui: TGetterOrReadonlyRef[str]):
        @self._ui_effect
        def _():
            ele = self.element
            ele._props["icon"] = to_value(ref_ui)
            ele.update()

        return self
