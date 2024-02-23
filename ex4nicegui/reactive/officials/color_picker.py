from typing import (
    Any,
    Callable,
    Optional,
    cast,
)
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.apiEffect import ui_effect

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    to_value,
)
from nicegui import ui
from nicegui.events import handle_event
from .base import BindableUi


class ColorPickerBindableUi(BindableUi[ui.color_picker]):
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
            v_model=("color", "on_pick"),
            v_model_arg_getter=lambda e: e.color,
            events=["on_pick"],
        )

        value_kws = pc.get_values_kws()

        with ui.card().tight():
            exclued_color = {**value_kws}
            exclued_color.pop("color")

            element_menu = ui.color_picker(**exclued_color)
            element_menu.set_color(value_kws.get("value") or "")

            self._element_picker = element_menu.default_slot.children[0]
            self._element_picker.props('format-model="rgba"')

            ui.button(on_click=element_menu.open, icon="colorize")

        super().__init__(element_menu)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef[str]):
        @ui_effect
        def _():
            self.element.set_color(to_value(ref_ui))

        return self

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))

        return self


class ColorPickerLazyBindableUi(ColorPickerBindableUi):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        org_value = value
        is_setter_value = is_setter_ref(value)
        if is_setter_value:
            value = to_value(value)

        super().__init__(color, on_pick=None, value=value)

        if is_setter_value:
            ref = cast(Ref, org_value)

            ele = self._element_picker

            def onModelValueChanged(e):
                ref.value = e.args  # type: ignore

                if on_pick:
                    handle_event(on_pick, e)

            ele.on("change", handler=onModelValueChanged)
