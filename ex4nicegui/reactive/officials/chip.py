from typing import Any, Callable, Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


class ChipBindableUi(BindableUi[ui.chip]):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        icon: Optional[TMaybeRef[str]] = None,
        color: Optional[TMaybeRef[str]] = "primary",
        text_color: Optional[TMaybeRef[str]] = None,
        on_click: Optional[Callable[..., Any]] = None,
        selectable: TMaybeRef[bool] = False,
        selected: TMaybeRef[bool] = False,
        on_selection_change: Optional[Callable[..., Any]] = None,
        removable: TMaybeRef[bool] = False,
        on_value_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "text",
                "icon",
                "color",
                "text_color",
                "selectable",
                "selected",
                "removable",
            ],
            events=[],
        )

        element = ui.chip(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def text(self):
        return self.element.text

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: TGetterOrReadonlyRef):
        """Binds the background color property of the chip element.

        Args:
            ref_ui (TGetterOrReadonlyRef): _description_
        """

        @self._ui_effect
        def _():
            ele = self.element
            color = to_value(ref_ui)
            ele._props["color"] = color
            ele.update()

    def bind_text(self, ref_ui: TGetterOrReadonlyRef):
        @self._ui_effect
        def _():
            self.element.set_text(str(to_value(ref_ui)))
            self.element.update()

        return self
