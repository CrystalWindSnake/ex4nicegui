from typing import (
    Any,
    Callable,
    Optional,
)
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import SingleValueBindableUi


class ColorPickerBindableUi(SingleValueBindableUi[str, ui.color_picker]):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        """Color Picker

        Args:
            color (TMaybeRef[str], optional): color value str. Defaults to "".
            on_pick (Optional[Callable[..., Any]], optional): callback to execute when a color is picked. Defaults to None.
            value (TMaybeRef[bool], optional): whether the menu is already opened. Defaults to False.
        """

        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "color",
                "value",
            ],
            events=["on_pick"],
        )

        value_kws = pc.get_values_kws()

        value_ref = to_ref(color)

        self._setup_on_change(value_ref, value_kws, on_pick)

        with ui.card().tight():
            exclued_color = {**value_kws}
            exclued_color.pop("color")

            element_menu = ui.color_picker(**exclued_color)
            element_menu.set_color(value_kws.get("value") or "")

            self._element_picker = element_menu.default_slot.children[0]
            self._element_picker.props('format-model="rgba"')

            ui.button(on_click=element_menu.open, icon="colorize")

        super().__init__(value_ref, element_menu)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef[str]):
        @effect
        def _():
            self.element.set_color(to_value(ref_ui))

        return self

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.set_value(to_value(ref_ui))

        return self

    def _setup_on_change(
        self,
        color_ref: Ref[str],
        value_kws: dict,
        on_pick: Optional[Callable[..., Any]] = None,
    ):
        def inject_on_change(e):
            color_ref.value = e.color
            if on_pick:
                handle_event(on_pick, e)

        value_kws.update({"on_pick": inject_on_change})


class ColorPickerLazyBindableUi(ColorPickerBindableUi):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        super().__init__(color, on_pick=None, value=value)

        ele = self._element_picker

        def onModelValueChanged(e):
            self._ref.value = e.args  # type: ignore

            if on_pick:
                handle_event(on_pick, e)

        ele.on("change", handler=onModelValueChanged)

    def _setup_on_change(
        self,
        color_ref: Ref[str],
        value_kws: dict,
        on_pick: Optional[Callable[..., Any]] = None,
    ):
        pass
